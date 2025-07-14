#!/bin/bash
# Step 4: Generate embeddings using Neo4j GenAI - wrapper for cypher script

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable not set"
    echo "Usage: export OPENAI_API_KEY='sk-...'"
    exit 1
fi

# Use NEO_NAME or default
NEO_NAME=${NEO_NAME:-neo4j-default}

echo "Generating embeddings in $NEO_NAME container..."
echo "Using OpenAI API key: ${OPENAI_API_KEY:0:7}..."

# Run the cypher script with proper parameter passing
docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! \
    --param "openai_api_key => '$OPENAI_API_KEY'" \
    < scripts/generate-embeddings.cypher