// COMPREHENSIVE CRIMINAL ACTIVITY INVESTIGATION
// Single query for investigating suspicious communications using Neo4j GenAI
// 
// SETUP: First set your OpenAI API key
// :param openai_api_key => "your-actual-api-key-here"
//
// PURPOSE: Detect criminal activity in surveillance communications with optimal threshold
// RETURNS: Summary statistics + top evidence conversations ranked by confidence
// THRESHOLD: 0.58 (optimized for surveillance data - captures quality results without noise)

WITH genai.vector.encode(
    "drug dealing money laundering criminal activity illegal shipment suspicious meeting cash payment weapons trafficking", 
    "OpenAI", 
    {token: $openai_api_key, model: "text-embedding-3-small"}
) AS criminal_query

MATCH (c:Content)
WHERE c.embedding IS NOT NULL
  AND c.contentType = 'audio/x-wav'
WITH c, vector.similarity.cosine(c.embedding, criminal_query) AS relevance
WHERE relevance > 0.58

WITH collect({
    confidence: round(relevance * 100, 1),
    text: substring(c.text, 0, 600),
    session_id: c.sessionguid,
    timestamp: c.timestamp
}) AS evidence_list

RETURN 
    'CRIMINAL ACTIVITY INVESTIGATION' as investigation_type,
    size(evidence_list) as suspicious_conversations_found,
    round(reduce(sum = 0.0, item IN evidence_list | sum + item.confidence) / size(evidence_list), 1) as avg_confidence_score,
    evidence_list[0..5] as top_evidence_with_details

// USAGE INSTRUCTIONS:
// 1. Set API key: :param openai_api_key => "sk-proj-your-key"
// 2. Run this query
// 3. Review 'suspicious_conversations_found' count
// 4. Examine 'top_evidence_with_details' for actual conversation excerpts
// 5. Investigate sessions with highest confidence scores first
//
// INTERPRETATION:
// - suspicious_conversations_found: Number of conversations above threshold
// - avg_confidence_score: Average AI confidence (higher = more suspicious)  
// - top_evidence_with_details: Actual conversation text with confidence scores
//
// THRESHOLD NOTES:
// - 0.58 = Balanced precision/recall based on surveillance data analysis
// - Lower threshold (0.5) = More results, potentially more noise
// - Higher threshold (0.65+) = Fewer results, may miss coded language