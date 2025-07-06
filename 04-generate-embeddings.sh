#!/bin/bash
# Step 4: Generate embeddings wrapper script
#
# This script provides a simple interface for generating embeddings
# using the Neo4j GenAI batch processing.
#
# Prerequisites:
#   1. OPENAI_API_KEY environment variable set
#   2. NEO_NAME environment variable set (or defaults to neo4j-default)
#
# Usage:
#   export OPENAI_API_KEY="sk-..."
#   ./04-generate-embeddings.sh

set -e

# Configuration
NEO_NAME=${NEO_NAME:-neo4j-default}

# Check prerequisites
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable not set"
    echo "   Please set it with: export OPENAI_API_KEY=\"sk-...\""
    exit 1
fi

# Check if container is running
if ! docker ps --filter "name=$NEO_NAME" --filter "status=running" | grep -q "$NEO_NAME"; then
    echo "❌ Error: Container $NEO_NAME is not running"
    echo "   Start it with: ./run_neo4j.sh"
    exit 1
fi

echo "Generating embeddings in $NEO_NAME container..."
echo "Using OpenAI API key: ${OPENAI_API_KEY:0:7}..."

# Run the embedding generation script
docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3! \
    --param "openai_api_key => '$OPENAI_API_KEY'" \
    < scripts/cypher/04-generate-embeddings.cypher

echo "✅ Embedding generation complete!"