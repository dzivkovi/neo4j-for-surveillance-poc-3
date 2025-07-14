# Embedding Generation Guide

Robust guide for generating OpenAI embeddings using Python script with resume capability.

## Quick Start (Recommended)

```bash
export OPENAI_API_KEY="sk-..."
./scripts/04-generate-embeddings.sh
```

**Features:**
- Resume capability if process stops
- Progress monitoring with logs
- Robust error handling
- Batch processing optimized for OpenAI API limits

## Manual Cypher Approach

For direct cypher-shell execution:

```bash
docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! <<EOF
:param openai_api_key => "$OPENAI_API_KEY"

MATCH (c:Content)
WHERE c.text IS NOT NULL AND c.embedding IS NULL
WITH collect(c) AS nodes
WITH nodes, [n IN nodes | substring(n.text, 0, 8000)] AS texts
CALL genai.vector.encodeBatch(texts, 'OpenAI', {
    token: \$openai_api_key,
    model: 'text-embedding-3-small',
    dimensions: 1536
}) YIELD index, vector
WITH nodes[index] AS node, vector
CALL db.create.setNodeVectorProperty(node, 'embedding', vector)
RETURN count(node) as nodes_embedded;
EOF
```

## Key Points

- Uses Neo4j GenAI plugin (must be enabled in container)
- Generates 1536-dimensional embeddings with OpenAI text-embedding-3-small
- Handles batches automatically
- Parameter passing: `:param` sets the API key for the session