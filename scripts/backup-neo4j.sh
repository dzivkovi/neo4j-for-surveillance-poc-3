#!/usr/bin/env bash
set -euo pipefail

# Neo4j backup script using neo4j-admin database dump
# Creates portable .dump files that can be restored on any Neo4j instance
#
# Usage: ./backup-neo4j.sh [dataset_name]
# Default: ./backup-neo4j.sh (uses "default" dataset)

DATASET=${1:-default}
NEO_NAME="neo4j-${DATASET}"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
DUMP_FILE="data/${DATASET}/neo4j-database-${TIMESTAMP}.dump"

echo "Creating database dump for Neo4j container: ${NEO_NAME}"
echo "Timestamp: ${TIMESTAMP}"
echo ""

# Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${NEO_NAME}$"; then
    echo "Error: Container ${NEO_NAME} does not exist"
    exit 1
fi

# Check if data directory exists
if [ ! -d "data/${DATASET}" ]; then
    echo "Creating data directory: data/${DATASET}"
    mkdir -p "data/${DATASET}"
fi

# Step 1: Stop the container (required for Community Edition)
echo "Step 1: Stopping ${NEO_NAME} container..."
docker stop "${NEO_NAME}"

# Step 2: Create the dump
echo "Step 2: Creating database dump..."
docker run --rm \
    --volumes-from "${NEO_NAME}" \
    -v "$(pwd)/data/${DATASET}:/backup:rw" \
    neo4j:5.26.7-community \
    bash -c "neo4j-admin database dump neo4j --to-stdout > /backup/neo4j-database-${TIMESTAMP}.dump"

# Step 3: Restart the container
echo "Step 3: Restarting ${NEO_NAME} container..."
docker start "${NEO_NAME}"

# Get dump file size
if [ -f "${DUMP_FILE}" ]; then
    DUMP_SIZE=$(ls -lh "${DUMP_FILE}" | awk '{print $5}')
    echo ""
    echo "✅ Backup created successfully!"
    echo "- File: ${DUMP_FILE}"
    echo "- Size: ${DUMP_SIZE}"
else
    echo "❌ Error: Dump file was not created"
    exit 1
fi

# List existing dumps
echo ""
echo "Existing dumps for ${DATASET}:"
ls -lh data/${DATASET}/*.dump 2>/dev/null | awk '{print $9 "\t" $5}' || echo "No dumps found"

# Restore instructions
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TO RESTORE THIS DUMP:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Stop the target container:"
echo "   docker stop ${NEO_NAME}"
echo ""
echo "2. Load the dump (overwrites existing data):"
echo "   docker run --rm \\"
echo "     --volumes-from ${NEO_NAME} \\"
echo "     -v \$(pwd)/${DUMP_FILE}:/dump.file \\"
echo "     neo4j:5.26.7-community \\"
echo "     neo4j-admin database load neo4j --from-stdin --overwrite-destination < /dump.file"
echo ""
echo "3. Start the container:"
echo "   docker start ${NEO_NAME}"
echo ""
echo "Note: The dump is portable and can be restored to any Neo4j 5.x instance"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"