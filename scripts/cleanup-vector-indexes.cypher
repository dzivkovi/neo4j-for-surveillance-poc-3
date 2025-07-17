/***************************************************************************
  Vector Index Cleanup Script
  ============================
  Purpose: Remove old vector indexes and ensure correct PascalCase index
           exists for OpenAI embeddings (following Neo4j conventions)
  
  Usage: docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cleanup-vector-indexes.cypher
***************************************************************************/

// Drop old incorrectly named indexes if they exist
DROP INDEX content_vector_index IF EXISTS;
DROP INDEX ContentVectorIndexV2 IF EXISTS;

// Ensure the correct PascalCase vector index exists (Neo4j convention)
CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS
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