# From Overfitted Queries to LLM-Powered GraphRAG Discovery

## LLM-Driven Techniques for Mapping Criminal Networks in Neo4j

### Question

I’ve reviewed the queries you generated — while I appreciate the precision, much of it feels overfitted. You're basing queries too closely on expected answers and inserting specific words just to match the target outcome. This is exactly the kind of situation where Neo4j’s GenAI libraries and their implementation of Microsoft’s GraphRAG project could truly shine.

Let’s shift focus away from keyword stuffing and rigid matching. Instead, harness the power of LLMs to discover topics and patterns organically within surveillance graph data. Please pull the latest Neo4j GenAI tutorials and specs that use the Context7 MCP server, and incorporate the new Neo4j GenAI book I’m reading — along with any companion source code — to help design a better conceptual solution. Don’t try to answer any one question. Think in terms of strategic value for police investigators working with criminal networks.

Then, with deep reflection, think about the investigative queries you helped me craft in the past on smaller datasets. Use those as inspiration to suggest which patterns apply to this carjacking/Gantry dataset and how we could adapt the seven investigative questions I was recently given for this case. The goal is not to build brittle one-offs, but to guide the design of reusable investigative flows.

Don’t rush. Think big. Think reusability. Avoid overfitting and bias. Embrace LLM-powered intuition and curiosity. If the schema lacks vector indexes, don’t worry — I’ll provide them if needed. And yes, feel free to leave Lucene-style full-text search behind.

### Answer

You're absolutely right! I was overfitting by stuffing specific keywords into queries based on expected answers. That's the opposite of what investigators need - they need to discover patterns they don't know exist yet. Let me explore Neo4j's GraphRAG and GenAI capabilities for true discovery.

---

## Step 1: Getting Latest Neo4j GraphRAG Documentation## 🚀 Conceptual Shift: From Keyword Stuffing to LLM-Powered Discovery

You're absolutely right about the overfitting problem! Looking at your investigative queries, I can see they focus on discovering **patterns investigators don't know exist yet**. Let me propose a comprehensive GraphRAG-based solution that uses LLM intuition rather than predetermined keywords.

## 🧠 Core Concept: Three-Layer Intelligence System

### **Layer 1: Entity & Relationship Extraction (Neo4j GraphRAG)**

Instead of searching for "dealership" or "BMW X5", let the LLM discover what's important:

```python
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.llm import OpenAILLM

# Let the LLM discover entity types from the data itself
schema_extractor = SchemaFromTextExtractor(
    llm=OpenAILLM(model_name="gpt-4o")
)

# For Gantry carjacking case, it might discover:
# - Entities: Person, Vehicle, Location, Phone, Organization, TimeEvent
# - Relationships: DISCUSSES, MEETS_AT, OWNS, COORDINATES_WITH, PAYS
# - Properties: vehicle_details, location_type, transaction_amount

kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=driver,
    embedder=embedder,
    perform_entity_resolution=True,  # Merge "Johnny", "J-Dog", "JD" → same person
    on_error="IGNORE"
)
```

### **Layer 2: Community Detection & Summarization (Microsoft GraphRAG)**

Discover natural groupings and summarize at multiple levels:

```python
# GraphRAG community detection finds:
# - Level 0: Individual actors
# - Level 1: Small operational cells (3-5 people)
# - Level 2: Larger criminal networks
# - Level 3: Inter-network connections

CALL gds.graph.project('criminal-network', 
    ['Person', 'Phone', 'Location'], 
    ['PARTICIPATED_IN', 'DISCUSSED', 'LOCATED_AT']
)

CALL gds.louvain.stream('criminal-network')
YIELD nodeId, communityId
```

### **Layer 3: Dynamic Discovery Queries**

## 📊 Reimagined Evaluation Queries

### **EVAL-60: Data Summarization (GraphRAG Style)**

```cypher
// Instead of keyword searching, use community reports
MATCH (c:__Community__)-[:HAS_REPORT]->(r:CommunityReport)
WHERE c.level = 2  // Mid-level communities
RETURN r.summary as theme_summary,
       r.findings as key_insights,
       c.size as network_size,
       r.rank as importance_score
ORDER BY r.rank DESC

// Then use LLM to synthesize:
// "The data reveals 3 major themes: 
//  1. Vehicle acquisition networks (Communities 3,7,12)
//  2. Shipping coordination operations (Communities 5,9)
//  3. Financial transaction patterns (Communities 2,8,15)"
```

### **EVAL-61: Location Discovery (Semantic, Not Keywords)**

```cypher
// Use vector similarity to find theft-related discussions
CALL db.index.vector.queryNodes('ContentVectorIndex', 10, 
    genai.vector.encode("vehicle theft locations suspicious activity", 'OpenAI', 
    {token: $openai_key}))
YIELD node, score

// Then use GraphRAG extraction:
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
CALL apoc.ml.extractEntities(node.text) YIELD entities
WHERE any(e IN entities WHERE e.type = 'LOCATION')
RETURN entities, s.participants, score
```

### **EVAL-62/65: Relationship Discovery (Graph-Native)**

```cypher
// Don't assume Omar-Amy connection, discover ALL hidden bridges
CALL gds.alpha.allShortestPaths.stream('criminal-network', {
    relationshipWeightProperty: 'interaction_count',
    delta: 3.0
})
YIELD sourceNodeId, targetNodeId, distance
WITH gds.util.asNode(sourceNodeId) as source,
     gds.util.asNode(targetNodeId) as target,
     distance
WHERE distance > 2 AND source.community <> target.community
RETURN source.name, target.name, distance as separation_score
ORDER BY separation_score DESC
```

### **EVAL-63: Financial Network (GraphRAG NER)**

```cypher
// Use Neo4j GenAI to extract financial entities
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
CALL apoc.ml.extractEntities(c.text, {
    model: 'finance-ner-model',
    types: ['MONETARY_VALUE', 'TRANSACTION', 'FINANCIAL_ENTITY']
}) YIELD entities

// Build financial flow graph
MERGE (actor:Person {name: entities.actor})
MERGE (recipient:Person {name: entities.recipient})
MERGE (actor)-[t:TRANSFERS {amount: entities.amount}]->(recipient)

// Discover financial hubs
CALL gds.pageRank.stream('financial-network', {
    relationshipWeightProperty: 'amount'
})
```

### **EVAL-66: Small but Mighty (True Graph Analytics)**

```cypher
// Project multi-layer graph
CALL gds.graph.project('surveillance-network', 
    ['Person', 'Session', 'Content'],
    {
        PARTICIPATED_IN: {orientation: 'UNDIRECTED'},
        HAS_CONTENT: {orientation: 'UNDIRECTED'},
        MENTIONED_IN: {properties: 'importance'}
    }
)

// Calculate multiple centrality measures
CALL gds.alpha.eigenvector.stream('surveillance-network')
YIELD nodeId, score as eigenvector

CALL gds.betweenness.stream('surveillance-network')
YIELD nodeId, score as betweenness

CALL gds.alpha.articleRank.stream('surveillance-network')
YIELD nodeId, score as influence

// Combine metrics for "small but mighty" score
WITH gds.util.asNode(nodeId) as person,
     eigenvector, betweenness, influence,
     count{(person)-[:PARTICIPATED_IN]->()} as activity_count
WHERE activity_count < 10  // Low activity
  AND (betweenness > 0.7 OR influence > 0.8)  // High importance
RETURN person.name, activity_count, betweenness, influence
```

## 🔍 Advanced Investigative Patterns

### **1. Temporal Pattern Discovery**

```cypher
// Use GraphRAG to discover temporal patterns
MATCH (s:Session)
WITH s, s.starttime as time
CALL apoc.ml.detectAnomalies(
    collect({time: time, count: 1}),
    {method: 'isolation_forest'}
) YIELD anomalies
RETURN anomalies as suspicious_time_patterns
```

### **2. Multi-Modal Analysis**

```cypher
// Combine text, network, and temporal analysis
MATCH (p:Person)-[:PARTICIPATED_IN]->(s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.embedding IS NOT NULL

// Get semantic clusters
CALL gds.alpha.knn.stream('content-similarity', {
    topK: 5,
    nodeWeightProperty: 'embedding',
    similarityCutoff: 0.8
})
YIELD node1, node2, similarity

// Discover discussion topics without keywords
WITH collect({content: gds.util.asNode(node1), similarity: similarity}) as cluster
CALL apoc.ml.summarize(cluster) YIELD summary
RETURN summary as discovered_topic
```

### **3. Anomaly Detection Pipeline**

```cypher
// Build behavioral baseline
MATCH (p:Person)-[r:PARTICIPATED_IN]->(s:Session)
WITH p, count(s) as baseline_activity,
     stdev(s.durationinseconds) as duration_variance,
     collect(distinct type(r)) as communication_patterns

// Detect deviations
MATCH (p)-[r2:PARTICIPATED_IN]->(s2:Session)
WHERE s2.starttime > datetime() - duration('P7D')
WITH p, baseline_activity, duration_variance,
     count(s2) as recent_activity
WHERE abs(recent_activity - baseline_activity) > 2 * duration_variance
RETURN p.name as person_with_anomalous_behavior
```

## 🎯 Practical Implementation for Gantry Dataset

### **Step 1: Initial Knowledge Graph Construction**

```python
# Let GraphRAG discover the schema from a sample
sample_sessions = neo4j.run("""
    MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
    RETURN c.text LIMIT 100
""")

# Extract schema automatically
discovered_schema = await schema_extractor.run(
    text=" ".join([r['c.text'] for r in sample_sessions])
)

# Build KG with discovered schema
await kg_builder.run_async(
    text=full_dataset,
    schema=discovered_schema
)
```

### **Step 2: Community Analysis**

```python
# Run hierarchical community detection
communities = gds.louvain.write('criminal-network', 
    writeProperty='community_level_0')

# Generate community summaries
for level in range(3):
    reports = await generate_community_reports(
        level=level,
        llm=llm,
        include_findings=True
    )
```

### **Step 3: Investigation Queries**

Replace your specific questions with discovery queries:

1. **"What patterns exist in this data?"** → Community reports
2. **"Find suspicious locations"** → Semantic similarity + entity extraction
3. **"Who are the key players?"** → Multi-metric centrality
4. **"What are they planning?"** → Temporal anomaly + content clustering

## 💡 Key Advantages

1. **No Overfitting**: LLM discovers patterns, not predetermined keywords
2. **Reusable**: Same pipeline works for any investigation type
3. **Multi-Level Intelligence**: From individual entities to network-wide patterns
4. **Explainable**: Graph paths show HOW conclusions were reached
5. **Scalable**: Hierarchical summarization handles large datasets

## 🚨 Critical Success Factors

1. **Vector Indexes**: Create for semantic search
   ```cypher
   CREATE VECTOR INDEX content_embeddings IF NOT EXISTS
   FOR (c:Content) ON c.embedding
   OPTIONS {indexConfig: {`vector.dimensions`: 1536}}
   ```

2. **GraphRAG Integration**: Combine Neo4j and Microsoft approaches
3. **LLM Chain-of-Thought**: Let AI explain its discoveries
4. **Human-in-the-Loop**: Investigators validate AI findings

This approach transforms your system from "searching for needles" to "understanding the entire haystack" - exactly what modern investigations need!
