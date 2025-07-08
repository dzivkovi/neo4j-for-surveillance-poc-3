# Open-Ended Topic Discovery: Moving Beyond Predefined Topics

**Challenge**: Current EVAL-47 uses "guilty until proven innocent" approach with predefined topic queries. Need methods for discovering "what are the topics people are talking about" without bias.

## Problem Analysis

**Current Limitation**: EVAL-47 searches for predetermined topics:
```cypher
{topic: 'Property Management & Landscaping', query: 'landscaping maintenance property equipment Eagles yard service'}
```

**Desired Capability**: Discover topics organically from the data itself, like:
- "What themes emerge from this communication dataset?"
- "What are people actually discussing?"
- "What unexpected patterns exist?"

## Approach 1: Vector-Based Content Clustering (Pure Cypher)

**Concept**: Use vector embeddings to find natural content clusters, then extract representative themes.

### Implementation Strategy

```cypher
// 1. Find content similarity clusters using k-means-like approach
WITH 0.7 AS similarity_threshold

// Start with a seed content item
MATCH (seed:Content) WHERE seed.embedding IS NOT NULL
WITH seed LIMIT 1

// Find all similar content using vector similarity  
MATCH (c:Content) WHERE c.embedding IS NOT NULL
WITH seed, c, vector.similarity.cosine(seed.embedding, c.embedding) AS similarity
WHERE similarity > similarity_threshold

// Group into clusters and extract representative text
WITH collect({content: c, similarity: similarity}) AS cluster_contents
UNWIND cluster_contents AS item

// Sample top representative texts from each cluster
WITH cluster_contents, 
     [x IN cluster_contents WHERE x.similarity > 0.8][0..5] AS representatives

// Extract themes using content analysis
RETURN size(cluster_contents) AS cluster_size,
       [rep IN representatives | substring(rep.content.text, 0, 200)] AS sample_texts,
       representatives[0].content.contentType AS content_type,
       avg([rep IN representatives | rep.similarity]) AS avg_similarity
```

**Advantages**:
- Pure Cypher, no external dependencies
- Works with existing embeddings
- Finds natural content groupings

**Limitations**:
- Requires manual threshold tuning
- No automatic theme labeling
- Limited clustering sophistication

## Approach 2: Community Detection + LLM Summarization (APOC + GDS)

**Concept**: Use graph algorithms to find natural communication communities, then ask LLM to extract topics from each community.

### Implementation Strategy

```cypher
// 1. Create community-based content aggregation
CALL gds.graph.project(
  'contentGraph',
  ['Content', 'Session', 'Person'],
  ['HAS_CONTENT', 'PARTICIPATED_IN']
)

// 2. Run community detection on communication patterns
CALL gds.louvain.stream('contentGraph')
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
WHERE node:Content

// 3. Aggregate content by community
WITH communityId, collect(node.text) AS community_texts
WHERE size(community_texts) >= 5  // Filter small communities

// 4. Use APOC ML to extract topics from each community
UNWIND community_texts AS texts
WITH communityId, apoc.text.join(texts[0..20], '\n') AS combined_text  // Sample for LLM

CALL apoc.ml.openai.chat([
  {role: 'system', content: 'Extract 3-5 main topics from these conversation excerpts. Return only topic names, one per line.'},
  {role: 'user', content: combined_text}
], $openai_api_key) YIELD value

RETURN communityId AS community,
       value AS discovered_topics,
       size(community_texts) AS conversation_count
```

**Advantages**:
- Leverages natural communication patterns
- Produces human-readable topic labels
- Respects graph structure

**Limitations**:
- Requires APOC Extended
- LLM costs for topic extraction
- Complex multi-step process

## Approach 3: RAG-Based Open Discovery (Recommended)

**Concept**: Use Neo4j's RAG capabilities with open-ended prompts to discover topics without preconceptions.

### Simple Implementation

```cypher
// Direct RAG query for topic discovery
CALL apoc.ml.rag(
  'content_embedding_index',  // Your existing vector index
  ['text', 'contentType', 'timestamp'],
  'What are the 10 most frequently discussed topics in these communications? For each topic, provide a brief description and list 2-3 example conversation excerpts that represent that topic.'
) YIELD value

RETURN value AS discovered_topics
```

### Advanced Multi-Pass Discovery

```cypher
// Pass 1: Broad topic discovery
CALL apoc.ml.rag(
  'content_embedding_index',
  ['text', 'contentType'],
  'Analyze all the conversations and identify the major themes being discussed. Group similar topics together and provide a hierarchical list.'
) YIELD value AS broad_topics

// Pass 2: Detailed analysis per discovered topic
WITH broad_topics
CALL apoc.ml.rag(
  'content_embedding_index',
  ['text', 'session_id', 'timestamp'],
  'For each major topic identified in: "' + broad_topics + '", find specific conversation examples and explain what people are actually saying about that topic.'
) YIELD value AS detailed_analysis

RETURN broad_topics, detailed_analysis
```

**Advantages**:
- Uses existing infrastructure
- Completely open-ended discovery
- Provides natural language explanations
- Can iterate and refine

**Limitations**:
- Requires APOC Extended
- LLM API costs
- Results vary with prompt engineering

## Approach 4: Graph-Aware Iterative Discovery

**Concept**: Combine graph structure analysis with semantic discovery for richer insights.

### Implementation Strategy

```cypher
// 1. Find conversation patterns by analyzing session structures
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.embedding IS NOT NULL
WITH s, collect(c) AS session_contents, 
     avg([content IN collect(c) | size(content.text)]) AS avg_message_length

// 2. Identify different conversation types by structure
WITH s, session_contents, avg_message_length,
     CASE 
       WHEN size(session_contents) = 1 THEN 'single_message'
       WHEN size(session_contents) BETWEEN 2 AND 5 THEN 'short_conversation'  
       WHEN size(session_contents) > 5 THEN 'extended_conversation'
     END AS conversation_type

// 3. Sample representative conversations of each type
WITH conversation_type, collect(session_contents) AS type_sessions
UNWIND type_sessions[0..3] AS sample_session  // Sample from each type

// 4. Extract topics specific to conversation patterns
WITH conversation_type, 
     apoc.text.join([c IN sample_session | c.text], '\n') AS combined_content

CALL apoc.ml.openai.chat([
  {role: 'system', content: 'Analyze this ' + conversation_type + ' and identify what topics people discuss in this format. Consider both explicit topics and communication patterns.'},
  {role: 'user', content: combined_content}
], $openai_api_key) YIELD value

RETURN conversation_type,
       value AS pattern_specific_topics
```

**Advantages**:
- Considers communication patterns
- Discovers topics related to conversation structure
- More nuanced than pure content analysis

## Approach 5: GraphRAG Python Implementation (Most Sophisticated)

**Concept**: Use neo4j-graphrag package for advanced topic discovery with retrieval patterns.

### Python Implementation

```python
from neo4j_graphrag import VectorCypherRetriever
from neo4j import GraphDatabase
import openai

# Initialize retriever with custom discovery query
retriever = VectorCypherRetriever(
    driver=GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password")),
    index_name="content_embedding_index",
    retrieval_query="""
    // Custom query to get content with context
    MATCH (content)-[:HAS_CONTENT]-(session:Session)
    MATCH (session)-[:PARTICIPATED_IN]-(person:Person)
    RETURN content.text AS text,
           content.contentType AS type,
           session.session_id AS session,
           collect(DISTINCT person.name) AS participants,
           score
    """,
    embedder=OpenAIEmbeddings()
)

# Open-ended topic discovery
def discover_topics():
    # Step 1: Broad discovery
    broad_result = retriever.search(
        query_text="What topics and themes are being discussed across all conversations?",
        top_k=50  # Get diverse sample
    )
    
    # Step 2: Extract patterns from results
    all_content = "\n".join([item.content for item in broad_result.items])
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analyze these conversation excerpts and identify 8-12 distinct topics. For each topic, provide: 1) Topic name, 2) Brief description, 3) How frequently it appears, 4) Key participants discussing it."},
            {"role": "user", "content": all_content}
        ]
    )
    
    return response.choices[0].message.content
```

**Advantages**:
- Most sophisticated analysis
- Flexible retrieval patterns
- Production-ready framework
- Rich context integration

**Limitations**:
- Requires Python environment
- More complex setup
- Additional dependencies

## Recommended Approach for Your Use Case

**For immediate implementation**: Start with **Approach 3 (RAG-Based)** because:

1. **Uses existing infrastructure**: Your content embeddings and vector index
2. **Zero additional setup**: Works with current APOC Extended
3. **Completely unbiased**: No predefined topic lists
4. **Natural language output**: Easy to understand and validate
5. **Iterative refinement**: Can adjust prompts based on results

### Sample Implementation

```cypher
// Open-ended topic discovery query
:param openai_api_key => "your-key-here"

CALL apoc.ml.rag(
  'content_embedding_index',
  ['text', 'contentType', 'timestamp'],
  'Analyze all these communications and discover what topics people are actually discussing. Provide 8-10 main topics with evidence from actual conversations. For each topic, include: topic name, brief description, example quotes, and estimated frequency.'
) YIELD value

RETURN value AS organic_topic_discovery
```

**For advanced implementation**: Progress to **Approach 5 (GraphRAG Python)** for:
- Custom retrieval patterns
- Sophisticated topic modeling
- Integration with your analysis pipeline
- Scalable production deployment

## Next Steps

1. **Test RAG discovery** with your current setup
2. **Compare results** with EVAL-47 predefined topics
3. **Identify gaps** between biased and unbiased discovery
4. **Iterate prompts** to improve discovery quality
5. **Consider GraphRAG** for production implementation

This approach transforms your surveillance analytics from "looking for specific criminal activity" to "discovering what's actually happening in the communications" - a much more powerful investigative capability.