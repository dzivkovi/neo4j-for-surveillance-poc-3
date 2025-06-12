/*
  Neo4j Surveillance PoC - Vector Search Verification Queries
  ===========================================================
  Purpose: Verify that vector embeddings and semantic search are working correctly
  
  Usage: Run these queries in Neo4j Browser after running the embedding script
*/

// ============================================
// 1. Check which Content nodes have embeddings
// ============================================
MATCH (c:Content)
RETURN 
  count(CASE WHEN c.embedding IS NOT NULL THEN 1 END) as WithEmbeddings,
  count(CASE WHEN c.embedding IS NULL THEN 1 END) as WithoutEmbeddings,
  count(*) as TotalContent;

// ============================================
// 2. View content that has embeddings
// ============================================
MATCH (c:Content)
WHERE c.embedding IS NOT NULL
RETURN c.id, substring(c.text, 0, 200) as TextPreview, size(c.embedding) as EmbeddingDimensions;

// ============================================
// 3. Check vector index status
// ============================================
SHOW INDEXES
WHERE name = 'ContentVectorIndex';

// ============================================
// 4. Find similar content using vector search
// ============================================
// This query finds content similar to the first embedded text
MATCH (c:Content)
WHERE c.embedding IS NOT NULL
WITH c.embedding as queryVector
LIMIT 1
// Search for similar content
CALL db.index.vector.queryNodes('ContentVectorIndex', 5, queryVector) 
YIELD node, score
RETURN node.id as ContentId, score, substring(node.text, 0, 100) as Preview
ORDER BY score DESC;

// ============================================
// 5. View content with their associated sessions
// ============================================
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.embedding IS NOT NULL
RETURN s.sessionguid, s.sessiontype, substring(c.text, 0, 150) as ContentPreview;

// ============================================
// 6. Cross-similarity between all embedded content
// ============================================
// Shows how similar each piece of content is to others
MATCH (c1:Content)
WHERE c1.embedding IS NOT NULL
WITH collect({id: c1.id, embedding: c1.embedding, text: substring(c1.text, 0, 50)}) as contents
UNWIND contents as content1
CALL db.index.vector.queryNodes('ContentVectorIndex', 3, content1.embedding) 
YIELD node as content2, score
WHERE content1.id <> content2.id
RETURN 
  content1.id as Content1_ID,
  content1.text as Content1_Preview,
  content2.id as Content2_ID, 
  substring(content2.text, 0, 50) as Content2_Preview,
  score as SimilarityScore
ORDER BY Content1_ID, score DESC;

// ============================================
// BONUS: Semantic search for specific concepts
// ============================================
// To search for specific concepts like "travel plans", you need to:
// 1. Generate an embedding for your search query using Python
// 2. Use that embedding in the vector search
// 
// Example Python code to generate search embedding:
// ```python
// from sentence_transformers import SentenceTransformer
// model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
// search_query = "travel plans vacation"
// query_embedding = model.encode(search_query).tolist()
// print(query_embedding)  # Copy this array
// ```
//
// Then use in Cypher:
// WITH [<paste embedding array here>] as searchVector
// CALL db.index.vector.queryNodes('ContentVectorIndex', 10, searchVector)
// YIELD node, score
// RETURN node.id, score, substring(node.text, 0, 200) as Preview
// ORDER BY score DESC;
