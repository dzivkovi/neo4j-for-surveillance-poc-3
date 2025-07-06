#!/usr/bin/env bash
# Export Neo4j schema and stats to a readable text file

set -euo pipefail

CASE_NAME=${1:-default}
NEO_NAME="neo4j-${CASE_NAME}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="data/${CASE_NAME}/schema-export-${TIMESTAMP}.txt"

mkdir -p "data/${CASE_NAME}"

echo "Exporting schema from ${NEO_NAME} to ${OUTPUT_FILE}..."

{
    echo "Neo4j Schema Export - ${CASE_NAME}"
    echo "Timestamp: $(date)"
    echo "Container: ${NEO_NAME}"
    echo "========================================"
    echo
    
    echo "## LABELS ##"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "CALL db.labels() YIELD label RETURN label ORDER BY label"
    echo
    
    echo "## NODE COUNTS ##"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC"
    echo
    
    echo "## RELATIONSHIP TYPES ##"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType ORDER BY relationshipType"
    echo
    
    echo "## RELATIONSHIP COUNTS ##"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "MATCH ()-[r]->() RETURN type(r) as type, count(r) as count ORDER BY count DESC"
    echo
    
    echo "## INDEXES ##"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "SHOW INDEXES"
    echo
    
    echo "## CONSTRAINTS ##"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "SHOW CONSTRAINTS"
    echo
    
    echo "## SAMPLE DATA ##"
    echo "### Person nodes (first 3):"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "MATCH (p:Person) RETURN p LIMIT 3"
    echo
    
    echo "### Session nodes (first 3):"
    docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<< "MATCH (s:Session) RETURN s LIMIT 3"
    echo

} > "${OUTPUT_FILE}"

echo "Export complete: ${OUTPUT_FILE}"
echo
echo "Quick stats:"
tail -n +6 "${OUTPUT_FILE}" | head -20