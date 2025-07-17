#!/usr/bin/env bash
set -euo pipefail

# Helper script to run dataset-specific Neo4j containers
# Usage: ./run_neo4j.sh [dataset_name]
# Default: ./run_neo4j.sh (uses "default" dataset)
#
# Note: For large datasets (250K+ nodes), use run-neo4j-optimized.sh
# which includes memory configuration to prevent OutOfMemoryError

DATASET=${1:-default}
NEO_NAME="neo4j-${DATASET}"

echo "Starting Neo4j container for dataset: ${DATASET}"
echo "Container name: ${NEO_NAME}"

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^${NEO_NAME}$"; then
    echo "Container ${NEO_NAME} already exists."
    
    # Check if it's running
    if docker ps --format '{{.Names}}' | grep -q "^${NEO_NAME}$"; then
        echo "Container ${NEO_NAME} is already running on ports 7474/7687"
        exit 0
    else
        echo "Starting existing container ${NEO_NAME}..."
        docker start "${NEO_NAME}"
        echo "Container ${NEO_NAME} started successfully"
        exit 0
    fi
fi

# Convenience: stop any container already bound to port 7474
RUNNING=$(docker ps --filter publish=7474 --format '{{.Names}}' | head -n1)
if [ -n "$RUNNING" ]; then
    echo "Stopping container using port 7474: ${RUNNING}"
    docker stop "$RUNNING"
fi

# Create and run new container with optimized memory for large datasets
echo "Creating new container ${NEO_NAME}..."
docker run --name "$NEO_NAME" \
  --memory=8g --memory-swap=8g \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/Sup3rSecur3! \
  -e NEO4J_PLUGINS='["apoc","graph-data-science","genai"]' \
  -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*,db.*,genai.* \
  -e NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.*,db.*,genai.* \
  -e NEO4J_apoc_export_file_enabled=true \
  -e NEO4J_apoc_import_file_enabled=true \
  -e NEO4J_apoc_import_file_use__neo4j__config=true \
  -e NEO4J_server_memory_heap_initial__size=4G \
  -e NEO4J_server_memory_heap_max__size=4G \
  -e NEO4J_server_memory_pagecache_size=4G \
  -e NEO4J_db_transaction_timeout=120s \
  -e NEO4J_db_lock_acquisition_timeout=120s \
  -d neo4j:5.26.7-community

echo ""
echo "Neo4j container ${NEO_NAME} is starting..."
echo "- Browser: http://localhost:7474"
echo "- Bolt: bolt://localhost:7687"
echo "- Credentials: neo4j/Sup3rSecur3!"
echo ""
echo "Memory Configuration:"
echo "- Container: 8GB limit"
echo "- Heap: 4GB (initial and max)"
echo "- Page Cache: 4GB"
echo ""
echo "To monitor: docker stats ${NEO_NAME}"
echo "To switch datasets: ./run_neo4j.sh <dataset_name>"
echo "To stop: docker stop ${NEO_NAME}"
echo "To remove: docker rm ${NEO_NAME}"