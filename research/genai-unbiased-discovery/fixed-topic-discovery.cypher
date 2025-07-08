// FIXED: Simple Topic Discovery Query Using Neo4j GenAI
// This query properly terminates with RETURN clause

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
ORDER BY content_count DESC

// USAGE:
// 1. Set API key: :param openai_api_key => "your-openai-key"
// 2. Run this query
// 3. Results show major topics with counts, confidence scores, and evidence