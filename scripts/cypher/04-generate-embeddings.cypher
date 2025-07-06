// ========================================
// Step 4: Generate embeddings for Content nodes
// ========================================
//
// This script generates 1536-dimensional OpenAI embeddings for all Content nodes
// that have text but no existing embeddings. Uses Neo4j GenAI batch processing
// for efficient embedding generation.
//
// Prerequisites:
//   1. Neo4j container running with GenAI plugin enabled
//   2. Schema created (scripts/01-create-schema.sh)
//   3. Sessions imported (02-import-sessions.py)
//   4. Transcripts imported (03-import-transcripts.py)
//   5. OPENAI_API_KEY environment variable set
//
// Usage:
//   export OPENAI_API_KEY="sk-..."
//   docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! \
//     --param "openai_api_key => '$OPENAI_API_KEY'" \
//     < scripts/cypher/04-generate-embeddings.cypher

// ========================================
// PART 1: Show initial state
// ========================================
RETURN "=== INITIAL EMBEDDING STATE ===" as message;

MATCH (c:Content)
RETURN 
  count(c) as total_content,
  count(c.text) as with_text,
  count(c.embedding) as with_embeddings;

// ========================================
// PART 2: Collect texts for embedding
// ========================================
RETURN "=== COLLECTING TEXTS FOR EMBEDDING ===" as message;

MATCH (c:Content)
WHERE c.text IS NOT NULL 
  AND c.embedding IS NULL
  AND trim(c.text) <> ""
WITH collect(c.text) as texts
RETURN size(texts) as texts_to_embed;

// ========================================
// PART 3: Generate embeddings using OpenAI
// ========================================
RETURN "=== GENERATING EMBEDDINGS ===" as message;

MATCH (c:Content)
WHERE c.text IS NOT NULL 
  AND c.embedding IS NULL
  AND trim(c.text) <> ""
WITH collect(c.text) as texts, collect(c) as nodes

CALL genai.vector.encodeBatch(texts, 'OpenAI', {
    token: $openai_api_key,
    model: 'text-embedding-3-small',
    dimensions: 1536
}) YIELD index, vector

WITH nodes[index] as node, vector
SET node.embedding = vector

RETURN count(*) as nodes_embedded;

// ========================================
// PART 4: Verify embeddings were created
// ========================================
RETURN "=== EMBEDDING VERIFICATION ===" as message;

MATCH (c:Content)
WHERE c.embedding IS NOT NULL
RETURN 
  count(*) as embeddings_count,
  min(size(c.embedding)) as min_dims,
  max(size(c.embedding)) as max_dims;

RETURN "=== EMBEDDING GENERATION COMPLETE ===" as message;