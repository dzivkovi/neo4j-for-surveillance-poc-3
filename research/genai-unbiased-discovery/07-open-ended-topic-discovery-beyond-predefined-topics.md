# Open-Ended Topic Discovery: Moving Beyond Predefined Topics

**Date**: 2025-07-08  
**Time**: Late evening session  
**Context**: User preparing for sleep, requesting analysis of unbiased topic discovery approaches

## User's Question and Requirements

User highlighted a critical limitation in the current EVAL-47 approach: it uses a "guilty until proven innocent" bias with predefined topic expectations. They requested exploration of more generic, open-ended approaches to answer questions like "what are the topics people are talking about" without predetermined bias.

**Key Challenge**: Move from searching for predetermined topics (Property Management, Betting, etc.) to discovering what topics actually emerge organically from the surveillance data.

**Resources Provided**: Neo4j GenAI documentation links and local tutorial files about GraphRAG capabilities.

## Analysis and Findings

### Current System Limitation

EVAL-47 currently uses predefined topic queries like:
```cypher
{topic: 'Property Management & Landscaping', query: 'landscaping maintenance property equipment Eagles yard service'}
```

This approach assumes we know what to look for, creating investigative bias.

### Five Recommended Approaches

After studying Neo4j GenAI capabilities and GraphRAG documentation, I identified five progressively sophisticated approaches:

#### 1. Vector-Based Content Clustering (Pure Cypher)
**Concept**: Use existing embeddings to find natural content clusters through similarity thresholds.

**Implementation**:
```cypher
WITH 0.7 AS similarity_threshold
MATCH (seed:Content) WHERE seed.embedding IS NOT NULL
WITH seed LIMIT 1
MATCH (c:Content) WHERE c.embedding IS NOT NULL
WITH seed, c, vector.similarity.cosine(seed.embedding, c.embedding) AS similarity
WHERE similarity > similarity_threshold
// Group into clusters and extract representative text
```

**Pros**: Pure Cypher, uses existing infrastructure  
**Cons**: Manual threshold tuning, no automatic theme labeling

#### 2. Community Detection + LLM Summarization
**Concept**: Use graph algorithms to find communication communities, then extract topics from each community.

**Implementation**: Combines GDS community detection with APOC ML topic extraction.

**Pros**: Leverages communication patterns, produces readable labels  
**Cons**: Complex multi-step process, requires APOC Extended

#### 3. RAG-Based Open Discovery (Recommended)
**Concept**: Use Neo4j's RAG capabilities with completely open-ended prompts.

**Implementation**:
```cypher
CALL apoc.ml.rag(
  'content_embedding_index',
  ['text', 'contentType', 'timestamp'],
  'What are the 10 most frequently discussed topics in these communications? For each topic, provide a brief description and list 2-3 example conversation excerpts.'
) YIELD value
```

**Pros**: Uses existing infrastructure, zero additional setup, completely unbiased  
**Cons**: LLM API costs, requires prompt engineering

#### 4. Graph-Aware Iterative Discovery
**Concept**: Combine graph structure analysis with semantic discovery for richer insights.

**Implementation**: Analyzes conversation patterns (single message, short conversation, extended conversation) and discovers topics specific to each pattern.

**Pros**: Considers communication structure, more nuanced analysis  
**Cons**: Complex implementation, multiple analysis passes

#### 5. GraphRAG Python Implementation (Most Sophisticated)
**Concept**: Use neo4j-graphrag package for advanced topic discovery with custom retrieval patterns.

**Implementation**: Python-based solution with VectorCypherRetriever and custom discovery queries.

**Pros**: Most sophisticated analysis, production-ready framework  
**Cons**: Requires Python environment, additional dependencies

### Key Technical Insights

1. **Existing Infrastructure Ready**: Current content embeddings and vector index can power unbiased discovery immediately
2. **RAG Capabilities**: APOC Extended provides powerful RAG functions that work with existing vector indexes
3. **No Re-ingestion Needed**: All approaches work with current graph structure and embeddings
4. **Iterative Refinement**: Results can be improved through prompt engineering and parameter tuning

### Recommended Implementation Strategy

**Immediate Implementation**: Start with RAG-based discovery (Approach 3) because:
- Uses existing content embeddings and vector index
- Zero additional setup required
- Completely unbiased discovery
- Natural language output for easy validation
- Iterative refinement through prompt adjustment

**Sample Query**:
```cypher
CALL apoc.ml.rag(
  'content_embedding_index',
  ['text', 'contentType'],
  'Analyze all these communications and discover what topics people are actually discussing. Provide 8-10 main topics with evidence from actual conversations.'
) YIELD value
```

**Advanced Implementation**: Progress to GraphRAG Python (Approach 5) for production deployment with custom retrieval patterns and sophisticated topic modeling.

## Business Impact

This approach transforms surveillance analytics from:
- **Before**: "Looking for specific criminal activity patterns" (biased)
- **After**: "Discovering what's actually happening in communications" (unbiased)

This represents a fundamental shift from confirmation bias to genuine discovery - much more powerful for investigations.

## Next Steps

1. Test RAG discovery with current setup
2. Compare results with EVAL-47 predefined topics
3. Identify gaps between biased and unbiased discovery
4. Iterate prompts to improve discovery quality
5. Consider GraphRAG Python for production implementation

## Technical Achievement

Successfully identified path to transform "guilty until proven innocent" approach into genuinely open-ended discovery using existing Neo4j GenAI capabilities, preserving all current infrastructure while enabling unbiased topic discovery for surveillance investigations.