/***************************************************************************
  Vector Index Cleanup Script
  ============================
  Purpose: Remove old CamelCase vector indexes and ensure correct snake_case
           index exists for OpenAI embeddings
  
  Usage: docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/cleanup-vector-indexes.cypher
***************************************************************************/

// Drop old CamelCase indexes if they exist
DROP INDEX ContentVectorIndex IF EXISTS;
DROP INDEX ContentVectorIndexV2 IF EXISTS;

// Ensure the correct snake_case vector index exists
CREATE VECTOR INDEX content_vector_index IF NOT EXISTS
FOR (c:Content) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: "COSINE"
  }
};

// Show final index status
SHOW INDEXES 
WHERE name CONTAINS 'vector' OR name CONTAINS 'Vector' OR name CONTAINS 'content'
YIELD name, state, type, populationPercent, properties
ORDER BY name;