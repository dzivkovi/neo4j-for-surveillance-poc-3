#!/bin/bash
# Setup Dataset metadata nodes for runtime identification

set -e

# Function to create dataset node
create_dataset_node() {
    local dataset_name=$1
    local display_name=$2
    local container_name="neo4j-${dataset_name}"
    
    echo "Creating Dataset node for ${dataset_name}..."
    
    # Check if container is running
    if ! docker ps | grep -q "${container_name}"; then
        echo "Warning: Container ${container_name} is not running"
        return 1
    fi
    
    # Create Dataset node
    docker exec -i ${container_name} cypher-shell -u neo4j -p Sup3rSecur3! <<EOF
// Create constraint first
CREATE CONSTRAINT dataset_singleton IF NOT EXISTS
FOR (d:Dataset)
REQUIRE d.name IS UNIQUE;

// Create or update Dataset node
MERGE (d:Dataset {name: '${dataset_name}'})
SET d.displayName = '${display_name}',
    d.containerName = '${container_name}',
    d.createdAt = coalesce(d.createdAt, datetime()),
    d.updatedAt = datetime(),
    d.version = '1.0'
RETURN d;
EOF
}

# Setup common datasets
echo "Setting up Dataset metadata nodes..."

# Check which containers are running
echo "Active Neo4j containers:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep neo4j || true

# Try to setup dataset nodes for common datasets
datasets=(
    "default:Default Dataset"
    "gantry:Operation Gantry"
    "bigdata:Large Scale Dataset"
    "clientA:Client A Dataset"
)

for dataset_info in "${datasets[@]}"; do
    IFS=':' read -r name display <<< "$dataset_info"
    create_dataset_node "$name" "$display" || true
done

echo "Dataset metadata setup complete!"
echo ""
echo "To verify, run:"
echo "docker exec -i neo4j-<dataset> cypher-shell -u neo4j -p Sup3rSecur3! -c 'MATCH (d:Dataset) RETURN d'"