// Generate OpenAI embeddings for Content nodes using Neo4j GenAI
// 
// Usage:
//   export OPENAI_API_KEY="sk-..."
//   docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! \
//     --param "openai_api_key => $OPENAI_API_KEY" \
//     < scripts/04-generate-embeddings.cypher
//
// Or use the convenience script: ./04-generate-embeddings.sh

// Check current embedding status
MATCH (c:Content)
RETURN 
    count(c) as total_content,
    count(c.text) as with_text,
    count(c.embedding) as with_embeddings;

// Generate embeddings for all nodes with text but no embeddings
MATCH (c:Content)
WHERE c.text IS NOT NULL AND c.embedding IS NULL
WITH collect(c) AS nodes
WITH nodes, [n IN nodes | substring(n.text, 0, 8000)] AS texts
WHERE size(texts) > 0
CALL genai.vector.encodeBatch(texts, 'OpenAI', {
    token: $openai_api_key,
    model: 'text-embedding-3-small',
    dimensions: 1536
}) YIELD index, vector
WITH nodes[index] AS node, vector
CALL db.create.setNodeVectorProperty(node, 'embedding', vector)
RETURN count(node) as nodes_embedded;

// Verify embedding dimensions
MATCH (c:Content)
WHERE c.embedding IS NOT NULL
RETURN 
    count(*) as embeddings_count,
    min(size(c.embedding)) as min_dims,
    max(size(c.embedding)) as max_dims;

// Create vector index if it doesn't exist
CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS
FOR (c:Content)
ON (c.embedding)
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 1536,
        `vector.similarity_function`: 'cosine'
    }
};