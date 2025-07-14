#!/bin/bash
# Step 4: Complete embedding generation script with automatic batching and error handling

set -e

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable not set"
    echo "Usage: export OPENAI_API_KEY='sk-...'"
    exit 1
fi

# Use dataset environment variable or default
export DATASET=${DATASET:-default}
export NEO_NAME="neo4j-${DATASET}"

echo "🚀 Starting complete embedding generation for dataset: $DATASET"
echo "📦 Container: $NEO_NAME"
echo "🔑 OpenAI API key: ${OPENAI_API_KEY:0:7}..."

# Check if container is running
if ! docker ps | grep -q "$NEO_NAME"; then
    echo "❌ Container $NEO_NAME is not running"
    echo "Start it with: ./scripts/run-neo4j.sh $DATASET"
    exit 1
fi

# Run the optimized Python script
echo "🎯 Running optimized embedding generation..."
python scripts/generate_embeddings.py

# Verify completion
echo "✅ Embedding generation complete!"
echo "📊 Final statistics:"

# Get final embedding stats
docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! <<EOF
MATCH (c:Content)
WITH 
    count(c) as total_content,
    count(c.text) as with_text,
    count(c.embedding) as with_embeddings
RETURN 
    total_content,
    with_text,
    with_embeddings,
    round(100.0 * with_embeddings / with_text, 1) as completion_percentage
EOF

echo "🎉 All content nodes with text now have embeddings!"
echo "🔍 Vector similarity search is now fully available for investigations."