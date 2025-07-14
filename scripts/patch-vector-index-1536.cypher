/***************************************************************************
  Vector Index Migration Patch: 384 → 1536 Dimensions
  =====================================================
  
  This patch safely migrates the existing ContentVectorIndex from 384 
  to 1536 dimensions to support OpenAI embeddings without losing data.
  
  IMPORTANT: This only updates the index schema. Existing embeddings will 
  need to be regenerated with the new 1536-dimension model.
  
  Usage: 
    docker exec ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/patch-vector-index-1536.cypher
***************************************************************************/

// Check current vector index status
SHOW INDEXES 
YIELD name, type, entityType, labelsOrTypes, properties
WHERE name = 'content_vector_index' OR name = 'ContentVectorIndex'
RETURN name, type, entityType, labelsOrTypes, properties;

// Drop the existing 384-dimension vector index
// This is safe - it only removes the index, not the embedding property or nodes
DROP INDEX content_vector_index IF EXISTS;
DROP INDEX ContentVectorIndex IF EXISTS;

// Create new 1536-dimension vector index
// Uses the standardized name from the schema
CREATE VECTOR INDEX ContentVectorIndex
FOR (c:Content) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: "COSINE"
  }
};

// Verify the new index was created correctly
SHOW INDEXES 
YIELD name, type, entityType, labelsOrTypes, properties
WHERE name = 'ContentVectorIndex'
RETURN name, type, entityType, labelsOrTypes, properties;

// Check how many Content nodes have embeddings
MATCH (c:Content)
WITH 
  count(*) as total_content,
  count(c.embedding) as with_embeddings,
  count(CASE WHEN c.embedding IS NOT NULL AND size(c.embedding) = 1536 THEN 1 END) as correct_dimensions,
  count(CASE WHEN c.embedding IS NOT NULL AND size(c.embedding) = 384 THEN 1 END) as old_dimensions
RETURN 
  total_content,
  with_embeddings,
  correct_dimensions as embeddings_1536_dim,
  old_dimensions as embeddings_384_dim,
  round(100.0 * correct_dimensions / with_embeddings, 2) as percent_correct_dims;