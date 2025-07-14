#!/usr/bin/env python
"""
Step 2: Import session data into Neo4j using the session-centric schema.

Load `data/whiskey-jack/sessions.ndjson` into Neo4j graph database. This creates the core
session nodes and all related entities (Person, Phone, Email, Device, Location).

Prerequisites:
  1. Neo4j container running
  2. Schema created (scripts/01-create-schema.sh)

Usage:
  python scripts/python/02-import-sessions.py
"""

import json
import pathlib
import urllib.parse
from datetime import datetime

from neo4j import GraphDatabase
from tqdm import tqdm

RAW_PATH = pathlib.Path(__file__).parent.parent.parent / "data" / "sessions.ndjson"
BOLT_URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Sup3rSecur3!")

driver = GraphDatabase.driver(BOLT_URI, auth=AUTH)


def dt(val: str):
    """Return ISO8601 string or None"""
    if not val:
        return None
    return val.replace("Z", "")  # Neo4j datetime() will accept it.


def create_aliases(tx, session_id, involvements):
    """Create alias nodes for all identifiers (Feature #7) - Fixed entity resolution"""
    for inv in involvements:
        person_name = inv.get("personname")
        if not person_name:
            continue  # Skip involvements without a person name

        # Create Person node with actual name (not anon-unknown)
        tx.run("MERGE (p:Person {name: $name})", name=person_name)

        # Create aliases for each identifier type
        identifiers = [
            ("msisdn", inv.get("msisdn")),
            ("imei", inv.get("imei")),
            ("email", inv.get("email")),
            ("nickname", inv.get("personname")),
        ]

        for alias_type, value in identifiers:
            if value:
                tx.run(
                    """
                    MERGE (a:Alias {rawValue: $value, type: $type})
                    WITH a
                    MATCH (p:Person {name: $name})
                    MERGE (a)-[:ALIAS_OF]->(p)
                """,
                    value=str(value),
                    type=alias_type,
                    name=person_name,
                )


def link_location(tx, session_id, location_data):
    """Link session to location if coordinates available (Feature #7)"""
    if location_data and location_data.get("latitude") and location_data.get("longitude"):
        try:
            lat = float(location_data["latitude"])
            lon = float(location_data["longitude"])
            tx.run(
                """
                MERGE (l:Location {geo: point({latitude: $lat, longitude: $lon})})
                WITH l
                MATCH (s:Session {sessionguid: $sid})
                MERGE (s)-[:LOCATED_AT]->(l)
            """,
                lat=lat,
                lon=lon,
                sid=session_id,
            )
        except (ValueError, TypeError):
            # Skip invalid coordinates
            pass


def ingest(tx, rec):
    # -------- Session --------------------------------------------------
    guid = rec["sessionguid"]

    # Create a clean properties dict with only primitive values
    session_props = {}
    for key, value in rec.items():
        # Skip complex nested structures
        if key not in ["involvements", "products", "fulltext", "enrichment_"]:
            if isinstance(value, (str, int, float, bool)) or value is None:
                session_props[key] = value
            elif isinstance(value, list) and all(isinstance(v, (str, int, float, bool)) for v in value):
                session_props[key] = value

    # Handle datetime conversions
    session_props["createddate"] = dt(session_props.get("createddate"))
    session_props["starttime"] = dt(session_props.get("starttime"))
    session_props["stoptime"] = dt(session_props.get("stoptime"))
    
    # Compute duration if missing but we have start and stop times
    if (session_props.get("starttime") and session_props.get("stoptime") and 
        not session_props.get("durationinseconds")):
        try:
            start = datetime.fromisoformat(session_props["starttime"])
            stop = datetime.fromisoformat(session_props["stoptime"])
            duration = int((stop - start).total_seconds())
            session_props["durationinseconds"] = duration
        except (ValueError, TypeError):
            pass  # Skip if parsing fails
    
    # Compute sessiondate from starttime for temporal queries
    if session_props.get("starttime"):
        # Store as ISO date string for Neo4j date() function
        session_props["sessiondate"] = session_props["starttime"].split("T")[0]

    tx.run(
        """
        MERGE (s:Session {sessionguid:$guid})
        SET  s += $props,
             s.createddate = CASE WHEN $props.createddate IS NULL
                                  THEN NULL
                                  ELSE datetime($props.createddate) END,
             s.starttime   = CASE WHEN $props.starttime IS NULL
                                  THEN NULL
                                  ELSE datetime($props.starttime) END,
             s.stoptime    = CASE WHEN $props.stoptime IS NULL
                                  THEN NULL
                                  ELSE datetime($props.stoptime) END,
             s.sessiondate = CASE WHEN $props.sessiondate IS NULL
                                  THEN NULL
                                  ELSE date($props.sessiondate) END
        """,
        guid=guid,
        props=session_props,
    )

    # -------- Involvements --------------------------------------------
    for inv in rec.get("involvements", []):
        person = inv.get("personname")
        phone = inv.get("msisdn")
        email = inv.get("email")
        imei = inv.get("imei")
        role = inv.get("role")

        if person:
            tx.run("MERGE (p:Person {name:$name})", name=person)

        # phone & Person link
        if phone:
            tx.run("MERGE (ph:Phone {number:$num})", num=phone)
            if person:
                tx.run(
                    """
                    MATCH (p:Person {name:$name}), (ph:Phone {number:$num})
                    MERGE (p)-[:USES]->(ph)
                """,
                    name=person,
                    num=phone,
                )

        # email
        if email:
            tx.run("MERGE (em:Email {email:$email})", email=email)
            if person:
                tx.run(
                    """
                    MATCH (p:Person {name:$name}), (em:Email {email:$email})
                    MERGE (p)-[:USES]->(em)
                """,
                    name=person,
                    email=email,
                )

        # device
        if imei:
            tx.run("MERGE (d:Device {imei:$imei})", imei=imei)
            if person:
                tx.run(
                    """
                    MATCH (p:Person {name:$name}),(d:Device {imei:$imei})
                    MERGE (p)-[:USES_DEVICE]->(d)
                """,
                    name=person,
                    imei=imei,
                )
            if phone:
                tx.run(
                    """
                    MATCH (d:Device {imei:$imei}),(ph:Phone {number:$num})
                    MERGE (d)-[:HAS_ACCOUNT]->(ph)
                """,
                    imei=imei,
                    num=phone,
                )

        # participation edge (phone/email if present, else person)
        if phone:
            tx.run(
                """
                MATCH (ph:Phone {number:$num}), (s:Session {sessionguid:$guid})
                MERGE (ph)-[r:PARTICIPATED_IN {role:$role}]->(s)
            """,
                num=phone,
                guid=guid,
                role=role,
            )
        elif email:
            tx.run(
                """
                MATCH (em:Email {email:$email}), (s:Session {sessionguid:$guid})
                MERGE (em)-[r:PARTICIPATED_IN {role:$role}]->(s)
            """,
                email=email,
                guid=guid,
                role=role,
            )
        elif person:
            tx.run(
                """
                MATCH (p:Person {name:$name}), (s:Session {sessionguid:$guid})
                MERGE (p)-[r:PARTICIPATED_IN {role:$role}]->(s)
            """,
                name=person,
                guid=guid,
                role=role,
            )

    # -------- Content (products) --------------------------------------
    for prod in rec.get("products", []):
        cid = prod.get("id") or prod.get("contentid")
        ctype = prod.get("contenttype")
        size = prod.get("size")
        text = None

        # if it's a text/vcard or text/plain
        if prod.get("contenttype_tltype", "").lower() == "text":
            if prod.get("uri", "").startswith("data:"):
                _, data_part = prod["uri"].split(",", 1)
                text = urllib.parse.unquote(data_part)
            elif rec.get("fulltext"):
                ft = rec["fulltext"]
                text = "\n".join(ft) if isinstance(ft, list) else ft

        tx.run(
            """
            MERGE (c:Content {id:$cid})
            SET   c.contentType = $ctype,
                  c.size = $size,
                  c.text = COALESCE($text, c.text)
            """,
            cid=cid,
            ctype=ctype,
            size=size,
            text=text,
        )
        tx.run(
            """
            MATCH (s:Session {sessionguid:$guid}), (c:Content {id:$cid})
            MERGE (s)-[:HAS_CONTENT]->(c)
        """,
            guid=guid,
            cid=cid,
        )

    # -------- Feature #7 Additions ------------------------------------
    # Create aliases for all involvements
    if "involvements" in rec:
        create_aliases(tx, guid, rec["involvements"])

    # Link location if available
    if "location" in rec:
        link_location(tx, guid, rec["location"])


with driver.session() as sess, open(RAW_PATH) as fh:
    for line in tqdm(fh, desc="Importing sessions"):
        sess.execute_write(ingest, json.loads(line))
print("✔ Import complete")
