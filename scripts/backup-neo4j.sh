#!/usr/bin/env bash
set -euo pipefail

# Neo4j backup script using Docker snapshots
# Usage: ./backup-neo4j.sh [dataset_name]
# Default: ./backup-neo4j.sh (uses "default" dataset)

DATASET=${1:-default}
NEO_NAME="neo4j-${DATASET}"
BACKUP_DATE=$(date +%Y-%m-%d)
SNAPSHOT_NAME="neo4j-${DATASET}-snapshot:${BACKUP_DATE}"

echo "Creating backup for Neo4j container: ${NEO_NAME}"
echo "Backup date: ${BACKUP_DATE}"

# Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${NEO_NAME}$"; then
    echo "Error: Container ${NEO_NAME} does not exist"
    exit 1
fi

# Create snapshot
echo "Creating Docker snapshot: ${SNAPSHOT_NAME}"
docker commit "${NEO_NAME}" "${SNAPSHOT_NAME}"

# Get snapshot info
SNAPSHOT_SIZE=$(docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" | grep "${SNAPSHOT_NAME}" | awk '{print $2}')

echo ""
echo "✅ Backup created successfully!"
echo "- Snapshot: ${SNAPSHOT_NAME}"
echo "- Size: ${SNAPSHOT_SIZE}"
echo ""
echo "To list all backups:"
echo "  docker images | grep neo4j-${DATASET}-snapshot"
echo ""
echo "To restore from this backup:"
echo "  docker stop ${NEO_NAME} && docker rm ${NEO_NAME}"
echo "  docker run -d --name ${NEO_NAME} --memory=8g -p 7474:7474 -p 7687:7687 ${SNAPSHOT_NAME}"
echo ""

# Optional: List all backups for this dataset
echo "Existing backups for ${DATASET}:"
docker images | grep "neo4j-${DATASET}-snapshot" | awk '{print $1":"$2"\t"$4" "$5" ago\t"$7}' | column -t

echo ""
echo "To create a database dump (requires stopping container):"
echo "  docker stop ${NEO_NAME}"
echo "  docker run --rm --volumes-from ${NEO_NAME} -v \$(pwd)/data/${DATASET}:/backup neo4j:5.26.7-community neo4j-admin database dump neo4j --to-stdout > data/${DATASET}/neo4j-database-${BACKUP_DATE}.dump"
echo "  docker start ${NEO_NAME}"