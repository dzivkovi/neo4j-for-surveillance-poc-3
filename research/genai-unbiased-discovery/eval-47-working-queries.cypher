// EVAL-47: Working Topic Discovery Queries (Fixed)
// Each query runs independently and produces results

// ============================================================================
// QUERY 1: SEMANTIC TOPIC DISCOVERY (Neo4j GenAI)
// ============================================================================

WITH [
  {topic: 'Criminal Activities', query: 'drug dealing money laundering criminal activity illegal shipment weapons trafficking'},
  {topic: 'Travel Planning', query: 'travel trip flight hotel booking destination meeting location'},
  {topic: 'Meeting Coordination', query: 'meeting arrangement schedule coordination time place tonight'},
  {topic: 'Financial Activities', query: 'money payment cash transfer bank account suspicious transactions'},
  {topic: 'Business Operations', query: 'business company work supplier order equipment landscaping maintenance'},
  {topic: 'Personal Communications', query: 'family personal relationship social friendship'}
] as topics

UNWIND topics as topic_info
WITH topic_info.topic as topic_name,
     genai.vector.encode(topic_info.query, "OpenAI", {token: $openai_api_key, model: "text-embedding-3-small"}) as query_vector

MATCH (c:Content)
WHERE c.embedding IS NOT NULL
WITH topic_name, query_vector, c, vector.similarity.cosine(c.embedding, query_vector) AS similarity
WHERE similarity > 0.6

WITH topic_name, 
     count(c) as content_count,
     round(avg(similarity) * 100, 2) as avg_relevance_score,
     collect({text: substring(c.text, 0, 150), confidence: round(similarity * 100, 1)})[0..3] as topic_examples

RETURN topic_name,
       content_count,
       avg_relevance_score,
       topic_examples
ORDER BY content_count DESC;

// ============================================================================
// QUERY 2: CONTENT TYPE DISTRIBUTION ANALYSIS
// ============================================================================

MATCH (c:Content)
WHERE c.text IS NOT NULL AND size(c.text) > 50 AND NOT c.text STARTS WITH '\u00a0'
WITH c.contentType as content_type, 
     c.sessionType as session_type,
     count(c) as type_count,
     collect(substring(c.text, 0, 120))[0..3] as type_examples
RETURN content_type, session_type, type_count, type_examples
ORDER BY type_count DESC
LIMIT 10;

// ============================================================================
// QUERY 3: TEMPORAL TOPIC EVOLUTION
// ============================================================================

MATCH (c:Content)
WHERE c.text IS NOT NULL 
  AND c.timestamp IS NOT NULL
  AND size(c.text) > 50
  AND NOT c.text STARTS WITH '\u00a0'
WITH substring(c.timestamp, 0, 10) as communication_date,
     c.contentType as content_type,
     count(c) as daily_count,
     collect(substring(c.text, 0, 100))[0..2] as daily_samples
WHERE daily_count >= 2
RETURN communication_date, content_type, daily_count, daily_samples
ORDER BY communication_date DESC, daily_count DESC
LIMIT 10;

// ============================================================================
// QUERY 4: NETWORK-BASED TOPIC PATTERNS
// ============================================================================

MATCH (p:Person)-[:PARTICIPATED_IN]->(s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.text IS NOT NULL AND size(c.text) > 100
WITH p.name as person_name, 
     s.sessionType as communication_type,
     count(c) as person_content_count,
     collect(DISTINCT substring(c.text, 0, 120))[0..2] as person_samples
WHERE person_content_count >= 3
RETURN person_name, communication_type, person_content_count, person_samples
ORDER BY person_content_count DESC
LIMIT 10;

// ============================================================================
// QUERY 5: SIMILARITY CLUSTER ANALYSIS
// ============================================================================

MATCH (c1:Content) 
WHERE c1.embedding IS NOT NULL 
WITH c1 ORDER BY rand() LIMIT 50

MATCH (c2:Content)
WHERE c2.embedding IS NOT NULL 
  AND elementId(c1) < elementId(c2)
WITH c1, c2, vector.similarity.cosine(c1.embedding, c2.embedding) as similarity
WHERE similarity > 0.85
RETURN count(*) as high_similarity_pairs,
       round(avg(similarity) * 100, 2) as avg_similarity_score,
       'Sampled clustering analysis (50 items)' as cluster_analysis
LIMIT 1;

// ============================================================================
// USAGE INSTRUCTIONS:
// 1. Set API key: :param openai_api_key => "your-openai-key"
// 2. Run each query separately (copy/paste sections)
// 3. Each query produces independent results for topic analysis
// 4. Combine results manually for comprehensive topic discovery
// ============================================================================