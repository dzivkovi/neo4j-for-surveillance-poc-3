"""
Load `data/sessions.ndjson` into Neo4j using the session-centric
schema.  Run AFTER 01-schema.cypher.
"""

import json
import pathlib
import urllib.parse

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
    session_props["endtime"] = dt(session_props.get("endtime"))

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
             s.endtime     = CASE WHEN $props.endtime IS NULL
                                  THEN NULL
                                  ELSE datetime($props.endtime) END
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


with driver.session() as sess, open(RAW_PATH) as fh:
    for line in tqdm(fh, desc="Importing sessions"):
        sess.execute_write(ingest, json.loads(line))
print("✔ Import complete")
