// EVAL-68: What phone numbers is Kenzie using?
CALL db.index.fulltext.queryNodes('AliasText', 'Kenzie') 
YIELD node
MATCH (node)-[:ALIAS_OF]->(p:Person)<-[:ALIAS_OF]-(phone:Alias {type: 'msisdn'})
RETURN 'EVAL-68' as test_id, 
       count(DISTINCT phone.rawValue) as phone_count,
       collect(DISTINCT phone.rawValue)[0..3] as sample_phones;

// EVAL-08: Are there any references to sago palms?
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago palms') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN 'EVAL-08' as test_id,
       count(*) as mention_count,
       avg(score) as avg_relevance;

// EVAL-06: Has Kenzie referenced a shed?
CALL db.index.fulltext.queryNodes('ContentFullText', 'shed') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(phone:Phone)-[:USED_BY]->(p:Person)
WHERE p.displayName CONTAINS 'Kenzie'
RETURN 'EVAL-06' as test_id,
       count(*) as shed_mentions,
       max(score) as best_match_score;

// EVAL-29: How many telephony sessions are longer than a minute?
MATCH (s:Session)
WHERE s.sessionType = 'Telephony' 
  AND s.durationInSeconds > 60
RETURN 'EVAL-29' as test_id,
       count(*) as long_calls,
       avg(s.durationInSeconds) as avg_duration_seconds;

// EVAL-43: Who are William Eagle's top associates?
CALL db.index.fulltext.queryNodes('AliasText', 'William OR Billy') 
YIELD node
MATCH (node)-[:ALIAS_OF]->(william:Person)
MATCH (william)<-[:USED_BY]-(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(otherPhone:Phone)-[:USED_BY]->(associate:Person)
WHERE associate <> william
RETURN 'EVAL-43' as test_id,
       associate.displayName as associate_name,
       count(s) as session_count
ORDER BY session_count DESC
LIMIT 5;

// SUMMARY: Overall Implementation Status
MATCH (s:Session)
OPTIONAL MATCH (s)-[:HAS_CONTENT]->(c:Content)
OPTIONAL MATCH (a:Alias)
RETURN 'SUMMARY' as test_id,
       count(DISTINCT s) as total_sessions,
       count(DISTINCT c) as sessions_with_content,
       count(DISTINCT a) as total_aliases,
       count(DISTINCT CASE WHEN a.type = 'msisdn' THEN a END) as phone_aliases,
       count(DISTINCT CASE WHEN s.sessionType = 'Telephony' THEN s END) as telephony_sessions;