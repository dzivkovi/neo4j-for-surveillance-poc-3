#!/bin/bash
# Step 1: Create complete Neo4j schema
#
# This script creates all constraints and indexes needed for the surveillance
# analytics POC. Uses individual commands for reliable execution.
#
# Usage: scripts/01-create-schema.sh

set -e

NEO_NAME=${NEO_NAME:-neo4j-default}

echo "Creating schema in $NEO_NAME container..."

# Check if container is running
if ! docker ps --filter "name=$NEO_NAME" --filter "status=running" | grep -q "$NEO_NAME"; then
    echo "❌ Error: Container $NEO_NAME is not running"
    echo "   Start it with: ./run_neo4j.sh"
    exit 1
fi

echo "Creating constraints..."
echo "CREATE CONSTRAINT session_guid IF NOT EXISTS FOR (s:Session) REQUIRE s.sessionguid IS UNIQUE;" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE CONSTRAINT phone_number IF NOT EXISTS FOR (p:Phone) REQUIRE p.number IS UNIQUE;" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE CONSTRAINT email_addr IF NOT EXISTS FOR (e:Email) REQUIRE e.email IS UNIQUE;" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE CONSTRAINT device_imei IF NOT EXISTS FOR (d:Device) REQUIRE d.imei IS UNIQUE;" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE CONSTRAINT alias_raw_unique IF NOT EXISTS FOR (a:Alias) REQUIRE a.rawValue IS UNIQUE;" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "Creating range indexes..."
echo "CREATE INDEX person_name_index IF NOT EXISTS FOR (p:Person) ON (p.name);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX session_createddate IF NOT EXISTS FOR (s:Session) ON (s.createddate);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX session_sessiontype IF NOT EXISTS FOR (s:Session) ON (s.sessiontype);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE RANGE INDEX sessionDuration IF NOT EXISTS FOR (s:Session) ON (s.durationinseconds);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "Creating investigative performance indexes..."
echo "CREATE INDEX content_sessionType IF NOT EXISTS FOR (c:Content) ON (c.sessionType);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX content_contentType IF NOT EXISTS FOR (c:Content) ON (c.contentType);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX content_target IF NOT EXISTS FOR (c:Content) ON (c.target);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX content_timestamp IF NOT EXISTS FOR (c:Content) ON (c.timestamp);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX session_casename IF NOT EXISTS FOR (s:Session) ON (s.casename);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX session_targetname IF NOT EXISTS FOR (s:Session) ON (s.targetname);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "Creating temporal analysis indexes (POLE-optimized)..."
echo "CREATE INDEX session_starttime IF NOT EXISTS FOR (s:Session) ON (s.starttime);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX session_stoptime IF NOT EXISTS FOR (s:Session) ON (s.stoptime);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX event_starttime IF NOT EXISTS FOR (e:Event) ON (e.starttime);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX event_endtime IF NOT EXISTS FOR (e:Event) ON (e.endtime);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "Creating POLE relationship performance indexes..."
echo "CREATE INDEX phone_participated IF NOT EXISTS FOR ()-[r:PARTICIPATED_IN]-() ON (r.timestamp);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3! || echo "Note: Relationship property indexes require Neo4j 5.x+"
echo "CREATE INDEX person_uses IF NOT EXISTS FOR ()-[r:USES]-() ON (r.since);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3! || echo "Note: Relationship property indexes require Neo4j 5.x+"
echo "CREATE INDEX session_direction IF NOT EXISTS FOR (s:Session) ON (s.direction);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX location_type IF NOT EXISTS FOR (l:Location) ON (l.type);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE INDEX device_type IF NOT EXISTS FOR (d:Device) ON (d.type);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "Creating full-text indexes..."
echo "CREATE FULLTEXT INDEX ContentFullText IF NOT EXISTS FOR (c:Content) ON EACH [c.text];" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
echo "CREATE FULLTEXT INDEX AliasText IF NOT EXISTS FOR (a:Alias) ON EACH [a.rawValue];" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "Creating spatial index..."
echo "CREATE POINT INDEX locationGeo IF NOT EXISTS FOR (l:Location) ON (l.geo);" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "Creating vector index..."
echo "CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS FOR (c:Content) ON (c.embedding) OPTIONS { indexConfig: { \`vector.dimensions\`: 1536, \`vector.similarity_function\`: \"COSINE\" } };" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!

echo "✅ Schema creation complete!"
echo ""
echo "Verifying schema..."
echo "SHOW CONSTRAINTS YIELD name;" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!