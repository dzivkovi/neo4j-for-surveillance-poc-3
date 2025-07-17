# Upgrade to Native Neo4j Vector Embeddings with Latest OpenAI Dimensions

## Problem / Metric
The current implementation uses 384-dimensional embeddings from a local sentence-transformers model (all-MiniLM-L6-v2), which limits semantic search accuracy and requires manual Python scripting for embedding generation. Modern OpenAI models provide significantly higher-quality embeddings (1536d for text-embedding-3-small, 3072d for text-embedding-3-large) and Neo4j v5 now supports native OpenAI integration through `genai.vector.encode()` functions.

**Measurable Impact:**
- Improve semantic search precision/recall for surveillance analytics
- Reduce operational complexity by eliminating manual embedding scripts
- Enable real-time embedding generation within Cypher queries
- Standardize on industry-leading embedding models

## Goal
Replace the current 384d local embedding system with Neo4j's native OpenAI integration using text-embedding-3-small (1536d) as the primary model, with graceful migration from existing embeddings and improved query performance.

## Scope (M/S/W)
- [M] Upgrade vector index to support 1536d embeddings (text-embedding-3-small)
- [M] Implement Neo4j native `genai.vector.encode()` for real-time embedding generation
- [M] Add OpenAI API key configuration and security
- [M] Migrate existing Content node embeddings to new dimensions
- [M] Update all vector search queries to use new index
- [S] Support configurable embedding model selection (3-small vs 3-large)
- [S] Implement batch embedding refresh functionality
- [S] Add embedding cost monitoring and optimization
- [W] Maintain backward compatibility with 384d embeddings
- [W] Support multiple embedding models simultaneously

## Acceptance Criteria
| # | Given | When | Then |
|---|-------|------|------|
| 1 | A Content node without embeddings | `genai.vector.encode()` is called on content text | 1536d vector is generated and stored using OpenAI API |
| 2 | Existing 384d embeddings in database | Migration script is executed | All Content nodes have new 1536d embeddings, old embeddings preserved as backup |
| 3 | Vector search query with text input | Query generates embedding and searches index | Results are returned using native Neo4j vector search with improved relevance |
| 4 | OpenAI API key is configured | System performs embedding operations | All operations use secure API key management without exposing credentials |
| 5 | Large batch of content needs embedding | Batch embedding function is used | Multiple texts are efficiently processed using `genai.vector.encodeBatch()` |
| 6 | GraphRAG queries are executed | Native embeddings are used for retrieval | Semantic search accuracy is improved over previous 384d system |

## Technical Design

### Architecture Changes
1. **Vector Index Upgrade**: Replace `ContentVectorIndex` (384d) with `ContentVectorIndexV2` (1536d)
2. **Native Embedding Integration**: Use Neo4j's `genai.vector.encode()` instead of Python scripts
3. **Configuration Management**: Add secure OpenAI API key handling via environment variables
4. **Migration Strategy**: Dual-index approach during transition, then cleanup

### Key Components

#### 1. Schema Updates
```cypher
// New 1536d vector index
CREATE VECTOR INDEX ContentVectorIndexV2 IF NOT EXISTS
FOR (c:Content) ON (c.embedding_v2)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: "COSINE"
  }
};
```

#### 2. Native Embedding Generation
```cypher
// Real-time embedding within queries
MATCH (c:Content) WHERE c.embedding_v2 IS NULL
CALL {
  WITH c
  CALL genai.vector.encode(c.text, 'OpenAI', {
    token: $openai_token,
    model: 'text-embedding-3-small'
  }) YIELD vector
  SET c.embedding_v2 = vector
} IN TRANSACTIONS OF 50 ROWS
```

#### 3. Environment Configuration
- `OPENAI_API_KEY`: Secure API key storage
- `EMBEDDING_MODEL`: Configurable model selection (default: text-embedding-3-small)
- `EMBEDDING_DIMENSIONS`: Model-specific dimensions (1536 for 3-small, 3072 for 3-large)

#### 4. Updated Vector Search Pattern
```cypher
// Semantic search with native embeddings
CALL genai.vector.encode($query_text, 'OpenAI', {token: $openai_token}) YIELD vector as query_vector
CALL db.index.vector.queryNodes('ContentVectorIndexV2', 10, query_vector) 
YIELD node, score
RETURN node.text, score ORDER BY score DESC
```

## Implementation Steps

1. **Update schema.cypher**: Add new 1536d vector index alongside existing 384d index
2. **Create migration script**: `scripts/cypher/04-migrate-embeddings.cypher` for batch re-embedding
3. **Add environment configuration**: Update Docker setup and documentation for OpenAI API key
4. **Modify GraphRAG demo**: Update `scripts/python/03-graphrag-demo.py` to use native embeddings
5. **Update vector search queries**: Replace manual embedding generation in all query files
6. **Create validation script**: Test embedding quality and search performance comparison
7. **Update documentation**: Revise CLAUDE.md with new embedding patterns and API key setup
8. **Clean up legacy**: Remove old Python embedding scripts and 384d index after migration

## Testing Strategy

### Pre-Migration Testing
- Validate OpenAI API connectivity and token authentication
- Test `genai.vector.encode()` function with sample content
- Benchmark embedding generation performance vs current Python approach

### Migration Testing
- Run migration on copy of production data
- Compare search result quality between 384d and 1536d embeddings
- Validate all existing queries work with new vector index
- Verify embedding dimensions and similarity scores

### Post-Migration Validation
- Execute comprehensive business requirements test suite
- Performance testing of vector search operations
- Cost analysis of OpenAI API usage vs local model
- Backup and rollback procedures

## Risks & Considerations

### Technical Risks
- **API Dependency**: OpenAI service availability affects embedding generation
- **Cost Management**: API usage costs vs current free local model
- **Migration Complexity**: Risk of data loss during vector index transition
- **Performance Impact**: Latency of API calls vs local embedding generation

### Mitigation Strategies
- **Fallback Option**: Maintain capability to switch back to local embeddings
- **Cost Controls**: Implement usage monitoring and batch optimization
- **Staged Migration**: Test with subset of data before full migration
- **Caching Strategy**: Cache frequently-used embeddings to reduce API calls

### Operational Considerations
- **API Key Security**: Secure credential management in deployment environments
- **Rate Limiting**: Handle OpenAI API rate limits gracefully
- **Monitoring**: Track embedding quality metrics and API usage
- **Documentation**: Clear upgrade path for development and production environments