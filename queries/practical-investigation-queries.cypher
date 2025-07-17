// =============================================================================
// PRACTICAL INVESTIGATION QUERIES FOR LAW ENFORCEMENT
// =============================================================================
// These queries focus on real investigative value rather than visual impressiveness

// =============================================================================
// 1. COMMUNICATION FREQUENCY ANALYSIS
// =============================================================================
// Find the most active communication pairs (potential conspirators)
MATCH (p1:Person)-[:USES]->(acc1)-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(acc2)<-[:USES]-(p2:Person)
WHERE p1 <> p2
WITH p1.name as person1, p2.name as person2, count(DISTINCT s) as total_sessions,
     collect(DISTINCT s.sessiontype) as communication_types,
     min(s.starttime) as first_contact,
     max(s.starttime) as last_contact
WHERE total_sessions >= 5
RETURN person1, person2, total_sessions, communication_types, first_contact, last_contact
ORDER BY total_sessions DESC;

// =============================================================================
// 2. DEVICE SHARING INVESTIGATION
// =============================================================================
// Find all people who have used the same devices (operational security breach)
MATCH (p1:Person)-[:USES_DEVICE]->(d:Device)<-[:USES_DEVICE]-(p2:Person)
WHERE p1 <> p2
WITH d.imei as device_id, collect(DISTINCT p1.name) + collect(DISTINCT p2.name) as users
RETURN device_id, users, size(users) as user_count
ORDER BY user_count DESC;

// =============================================================================
// 3. BURNER PHONE DETECTION
// =============================================================================
// Find phones used for very few sessions (potential burner phones)
MATCH (ph:Phone)-[:PARTICIPATED_IN]->(s:Session)
WITH ph.number as phone_number, count(DISTINCT s) as session_count,
     collect(DISTINCT s.sessiontype) as session_types,
     min(s.starttime) as first_use,
     max(s.starttime) as last_use
WHERE session_count <= 5
RETURN phone_number, session_count, session_types, first_use, last_use,
       duration.between(datetime(first_use), datetime(last_use)).days as days_active
ORDER BY session_count ASC;

// =============================================================================
// 4. NIGHT OWL ANALYSIS
// =============================================================================
// Find people who primarily communicate during suspicious hours (11 PM - 5 AM)
MATCH (p:Person)-[:USES]->(acc)-[:PARTICIPATED_IN]->(s:Session)
WHERE s.starttime IS NOT NULL
WITH p, s, time(s.starttime).hour as hour
WHERE hour >= 23 OR hour <= 5
WITH p.name as person, count(DISTINCT s) as night_sessions
MATCH (p2:Person {name: person})-[:USES]->(acc2)-[:PARTICIPATED_IN]->(s2:Session)
WITH person, night_sessions, count(DISTINCT s2) as total_sessions,
     round(100.0 * night_sessions / count(DISTINCT s2), 1) as night_percentage
WHERE night_percentage > 30
RETURN person, night_sessions, total_sessions, night_percentage
ORDER BY night_percentage DESC;
// Whiskey Jack Dataset Results: Fred Merlin (33.3% night activity), Ray (33.3%), Stommel family (50% but only 2 sessions)

// =============================================================================
// 5. COMMUNICATION HUB IDENTIFICATION
// =============================================================================
// Find people who act as bridges between different groups
MATCH (hub:Person)-[:USES]->(acc1)-[:PARTICIPATED_IN]->(s1:Session)<-[:PARTICIPATED_IN]-(acc2)<-[:USES]-(contact:Person)
WHERE hub <> contact
WITH hub.name as hub_person, count(DISTINCT contact) as unique_contacts,
     count(DISTINCT s1) as total_sessions
WHERE unique_contacts >= 10
RETURN hub_person, unique_contacts, total_sessions,
       round(1.0 * total_sessions / unique_contacts, 1) as avg_sessions_per_contact
ORDER BY unique_contacts DESC;

// =============================================================================
// 6. ENCRYPTED COMMUNICATION DETECTION
// =============================================================================
// Find sessions with encrypted or encoded content
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.text =~ '.*([A-Za-z0-9+/]{20,}|BEGIN PGP|-----BEGIN|[0-9a-fA-F]{32,}).*'
   OR c.text =~ '.*(encrypted|cipher|key|password).*'
RETURN s.sessionguid, s.sessiontype, s.targetname, 
       substring(c.text, 0, 200) as content_preview
LIMIT 20;

// =============================================================================
// 7. MULTI-DEVICE USER ANALYSIS
// =============================================================================
// Find people using multiple devices (operational security awareness)
MATCH (p:Person)-[:USES_DEVICE]->(d:Device)
WITH p.name as person, collect(d.imei) as devices, count(d) as device_count
WHERE device_count > 1
MATCH (p2:Person {name: person})-[:USES_DEVICE]->(d2:Device)-[:HAS_ACCOUNT]->(ph:Phone)
WITH person, devices, device_count, collect(DISTINCT ph.number) as phone_numbers
RETURN person, device_count, devices, phone_numbers
ORDER BY device_count DESC;

// =============================================================================
// 8. CALL DURATION ANOMALIES
// =============================================================================
// Find unusually long calls (Telephony sessions longer than 2 minutes)
MATCH (s:Session)
WHERE s.sessiontype = 'Telephony' AND s.durationinseconds IS NOT NULL
WITH s, s.durationinseconds as duration_seconds
WHERE duration_seconds > 120  // Calls longer than 2 minutes
MATCH (s)<-[:PARTICIPATED_IN]-(ph:Phone)<-[:USES]-(p:Person)
WITH s.sessionguid as sessionguid, s.targetname as targetname, 
     duration_seconds as duration_seconds,
     s.starttime as starttime, collect(DISTINCT p.name) as participants
RETURN sessionguid, targetname, duration_seconds, starttime, participants
ORDER BY duration_seconds DESC;
// Whiskey Jack Dataset Results: Found 2 long calls - Owen/Kenzie (192s), Ted/William/Richard (145s)

// =============================================================================
// 9. COMMUNICATION PATTERN CHANGES
// =============================================================================
// Detect sudden changes in communication patterns (before/after a date)
WITH datetime('2020-02-15T00:00:00') as cutoff_date
MATCH (p:Person)-[:USES]->(acc)-[:PARTICIPATED_IN]->(s:Session)
WHERE s.starttime IS NOT NULL
WITH p, s, cutoff_date,
     CASE WHEN datetime(s.starttime) < cutoff_date THEN 'before' ELSE 'after' END as period
WITH p.name as person, period, count(DISTINCT s) as session_count
WITH person, 
     sum(CASE WHEN period = 'before' THEN session_count ELSE 0 END) as before_count,
     sum(CASE WHEN period = 'after' THEN session_count ELSE 0 END) as after_count
WHERE before_count > 0 AND after_count > 0
RETURN person, before_count, after_count,
       round(100.0 * (after_count - before_count) / before_count, 1) as percent_change
ORDER BY abs(percent_change) DESC;
// Whiskey Jack Dataset Results: Fiona Finch +800%, Kenzie Hawk +410%, Richard Eagle -91.9% after Feb 2020

// =============================================================================
// 10. FIND SHORTEST PATH BETWEEN SUSPECTS
// =============================================================================
// Find how two people are connected through the network
// Replace the names with your persons of interest
MATCH path = shortestPath(
  (p1:Person {name: 'Eagle, Richard'})-[*1..6]-(p2:Person {name: 'Hawk, Kenzie'})
)
RETURN path,
       [node in nodes(path) WHERE node:Person | node.name] as people_in_path,
       length(path) as degrees_of_separation;

// =============================================================================
// 11. GROUP DETECTION VIA COMMON SESSIONS
// =============================================================================
// Find groups of 3+ people who frequently communicate together
MATCH (s:Session)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
WITH s, collect(DISTINCT p.name) as participants
WHERE size(participants) >= 3
RETURN participants, count(s) as multi_party_sessions
ORDER BY multi_party_sessions DESC;

// =============================================================================
// 12. CONTENT KEYWORD SEARCH
// =============================================================================
// Search for specific keywords in communications
// Modify the keywords list as needed
WITH ['money', 'payment', 'transfer', 'cash', 'bitcoin', 'meet', 'location'] as keywords
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE any(keyword IN keywords WHERE toLower(c.text) CONTAINS keyword)
WITH s, c, [keyword IN keywords WHERE toLower(c.text) CONTAINS keyword] as found_keywords
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid, s.sessiontype, collect(DISTINCT p.name) as participants,
       found_keywords, substring(c.text, 0, 200) as content_preview
LIMIT 20;

// =============================================================================
// 13. LONGEST SESSIONS BY TYPE
// =============================================================================
// Find the longest sessions of each type - useful for identifying important events
MATCH (s:Session)
WHERE s.durationinseconds IS NOT NULL AND s.durationinseconds > 0
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
WITH s.sessiontype as session_type, s.sessionguid as session_id, s.targetname as target,
     s.durationinseconds as duration, s.starttime as start_time,
     collect(DISTINCT p.name) as participants
RETURN session_type, session_id, target, duration, start_time, participants
ORDER BY duration DESC
LIMIT 20;

// =============================================================================
// 14. DEVICE USAGE ANALYSIS BY PERSON
// =============================================================================
// Find all phone numbers used by a specific person (adapted from EVAL-69)
// Replace the person name with your person of interest
MATCH (person:Person {name: '@Eagle, William'})-[:USES]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
WITH person, count(DISTINCT s) as total_sessions_for_person
MATCH (person)-[:USES]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
WITH person.name as person_name, phone.number as phone_number, 
     count(DISTINCT s) as sessions_using_phone,
     total_sessions_for_person
RETURN person_name, phone_number, sessions_using_phone,
       round(100.0 * sessions_using_phone / total_sessions_for_person, 1) as usage_percentage,
       total_sessions_for_person as total_sessions
ORDER BY sessions_using_phone DESC;
// Whiskey Jack Dataset Results: William uses 9366351931 for 74 sessions (93.7%), 9364254000 for 5 sessions (6.3%)

// =============================================================================
// 15. IMEI TRACKING AND DEVICE ANALYSIS
// =============================================================================
// Find all IMEIs associated with a specific person (adapted from EVAL-70)
// Replace the person name with your person of interest
MATCH (person:Person {name: '@Hawk, Kenzie'})-[:USES_DEVICE]->(d:Device)
OPTIONAL MATCH (d)-[:HAS_ACCOUNT]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN person.name as person_name,
       collect(DISTINCT d.imei) as imeis,
       count(DISTINCT d.imei) as device_count,
       count(DISTINCT s) as total_sessions_across_devices
ORDER BY device_count DESC;

// =============================================================================
// 16. EMAIL RELATIONSHIP ANALYSIS
// =============================================================================
// Analyze email exchanges between specific contacts (adapted from EVAL-76)
// Replace email addresses with your contacts of interest
MATCH (email1:Email {email: 'ziezieken88@gmail.com'})-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(email2:Email {email: 'jadog83@gmail.com'})
OPTIONAL MATCH (s)-[:HAS_CONTENT]->(c:Content)
RETURN email1.email as contact1,
       email2.email as contact2,
       count(DISTINCT s) as email_exchanges,
       collect(substring(c.text, 0, 200))[0..3] as content_samples,
       min(s.starttime) as first_exchange,
       max(s.starttime) as last_exchange
ORDER BY email_exchanges DESC;

// =============================================================================
// 17. FULL-TEXT CONTENT SEARCH
// =============================================================================
// Search for specific keywords in all communications content
// Modify the search term as needed
CALL db.index.fulltext.queryNodes('ContentFullText', 'shed OR meeting OR location') 
YIELD node, score
MATCH (s:Session)-[:HAS_CONTENT]->(node)
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid as session_id,
       s.sessiontype as session_type,
       collect(DISTINCT p.name) as participants,
       score as relevance_score,
       substring(node.text, 0, 300) as content_preview
ORDER BY score DESC
LIMIT 20;
// Whiskey Jack Dataset Results: Found 6 results - calendar events about drinks/location, emails about trip meetings

// =============================================================================
// 18. SEMANTIC SEARCH WITH VECTOR SIMILARITY
// =============================================================================
// Search for semantically similar content using vector embeddings
// This requires content to have embeddings generated first
MATCH (c:Content)
WHERE c.embedding IS NOT NULL
WITH c.embedding as queryVector
LIMIT 1
CALL db.index.vector.queryNodes('ContentVectorIndex', 10, queryVector) 
YIELD node, score
MATCH (s:Session)-[:HAS_CONTENT]->(node)
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid as session_id,
       collect(DISTINCT p.name) as participants,
       score as similarity_score,
       substring(node.text, 0, 200) as content_preview
ORDER BY similarity_score DESC;
// Whiskey Jack Dataset Results: Semantic search working! Finds VCARD contacts, business emails with 0.99+ similarity scores

// =============================================================================
// 19. SESSION CLASSIFICATION ANALYSIS
// =============================================================================
// Analyze sessions by classification status for investigation prioritization
MATCH (s:Session)
WITH count(*) as total_sessions
MATCH (s:Session)
WITH s.classification as classification, s.reviewstatus as review_status, 
     count(*) as session_count, total_sessions
RETURN classification, review_status, session_count,
       round(100.0 * session_count / total_sessions, 1) as percentage
ORDER BY session_count DESC;
// Whiskey Jack Dataset Results: Non-Pertinent 40.8%, Unknown 29.1%, Pertinent 24.5%, others <5%

// =============================================================================
// 20. AUDIO CONTENT DETECTION
// =============================================================================
// Find sessions containing audio content for transcript analysis
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.contentType STARTS WITH 'audio/'
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid as session_id,
       s.sessiontype as session_type,
       s.durationinseconds as duration_seconds,
       collect(DISTINCT p.name) as participants,
       c.contentType as audio_format
ORDER BY duration_seconds DESC;
// Whiskey Jack Dataset Results: Found 42 audio files, longest calls are Kenzie/Owen (192s), William/Richard/Ted (145s)

// =============================================================================
// 21. PERSON-TO-PERSON COMMUNICATION ANALYSIS
// =============================================================================
// Analyze how two specific people communicate (adapted from validation suite)
// Replace names with your persons of interest
MATCH (p1:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(p2:Person)
WHERE p1.name CONTAINS 'Kenzie' AND p2.name CONTAINS 'Owen'
RETURN p1.name as person1,
       p2.name as person2,
       s.sessiontype as communication_type,
       count(*) as session_count,
       min(s.starttime) as first_contact,
       max(s.starttime) as last_contact
ORDER BY session_count DESC;

// =============================================================================
// 22. TOP ASSOCIATES BY INTERACTION FREQUENCY
// =============================================================================
// Find the top associates of a specific person (adapted from validation suite)
// Replace the person name with your person of interest
MATCH (target:Person {name:'@Eagle, William'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(associate:Person)
WHERE associate.name <> '@Eagle, William'
WITH target, count(DISTINCT s) as total_target_sessions
MATCH (target)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(associate:Person)
WHERE associate.name <> '@Eagle, William'
WITH target.name as target_person, associate.name as associate, 
     count(DISTINCT s) as interactions,
     total_target_sessions
RETURN target_person, associate, interactions,
       round(100.0 * interactions / total_target_sessions, 1) as percentage_of_communications
ORDER BY interactions DESC
LIMIT 10;
// Whiskey Jack Dataset Results: Richard Eagle 36.7%, Fred Merlin 20.3%, Kenzie Hawk 15.2%, others <10%

// =============================================================================
// 23. PHONE-TO-IMEI MAPPING ANALYSIS
// =============================================================================
// Find which IMEIs are associated with a specific phone number (from validation suite)
// Replace phone number with your number of interest
MATCH (phone:Phone {number:'9366351931'})<-[:HAS_ACCOUNT]-(device:Device)
OPTIONAL MATCH (device)<-[:USES_DEVICE]-(person:Person)
RETURN phone.number as phone_number,
       collect(DISTINCT device.imei) as associated_imeis,
       count(DISTINCT device.imei) as imei_count,
       collect(DISTINCT person.name) as device_users
ORDER BY imei_count DESC;

// =============================================================================
// 24. MULTI-USER DEVICE ANALYSIS
// =============================================================================
// Find who has been using devices with a specific IMEI (from validation suite)
// Replace IMEI with your device of interest
MATCH (device:Device {imei:'359847107165930'})<-[:USES_DEVICE]-(person:Person)
OPTIONAL MATCH (device)-[:HAS_ACCOUNT]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN device.imei as imei,
       collect(DISTINCT person.name) as device_users,
       count(DISTINCT person.name) as user_count,
       count(DISTINCT s) as total_sessions,
       collect(DISTINCT phone.number) as associated_phones
ORDER BY user_count DESC;

// =============================================================================
// 25. EMAIL ADDRESS DISCOVERY
// =============================================================================
// Find email addresses used by a specific person (from validation suite)
// Replace name pattern with your person of interest
MATCH (person:Person)-[:USES]->(email:Email)
WHERE person.name CONTAINS 'Kenzie'
RETURN person.name as person_name,
       collect(DISTINCT email.email) as email_addresses,
       count(DISTINCT email.email) as email_count
ORDER BY email_count DESC;

// =============================================================================
// 26. TELEPHONY SESSION DURATION ANALYSIS
// =============================================================================
// Analyze long telephony sessions for detailed investigation (from validation suite)
MATCH (s:Session)
WHERE s.sessiontype = 'Telephony' AND s.durationinseconds > 60
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN count(*) as long_call_count,
       avg(s.durationinseconds) as avg_duration_seconds,
       max(s.durationinseconds) as longest_call_seconds,
       collect(DISTINCT p.name)[0..5] as frequent_callers
ORDER BY avg_duration_seconds DESC;

// =============================================================================
// 27. ALIAS SYSTEM PHONE NUMBER SEARCH
// =============================================================================
// Advanced phone number search using the alias system (from validation suite)
// Replace name with your person of interest
CALL db.index.fulltext.queryNodes('AliasText', 'Kenzie') 
YIELD node
MATCH (node)-[:ALIAS_OF]->(person:Person)<-[:ALIAS_OF]-(phone_alias:Alias {type: 'msisdn'})
RETURN person.name as person_name,
       count(DISTINCT phone_alias.rawValue) as phone_count,
       collect(DISTINCT phone_alias.rawValue) as all_phone_numbers
ORDER BY phone_count DESC;

// =============================================================================
// 28. MULTI-COMMUNICATION METHOD ANALYSIS
// =============================================================================
// Find people using multiple communication methods (from data exploration)
MATCH (person:Person)-[:USES]->(comm)
WITH person, collect(labels(comm)[0] + ': ' + COALESCE(comm.number, comm.email, 'N/A')) as communication_methods
WHERE size(communication_methods) > 1
RETURN person.name as person_name,
       communication_methods,
       size(communication_methods) as method_count
ORDER BY method_count DESC;

// =============================================================================
// 29. COMMUNICATION PAIRS FREQUENCY
// =============================================================================
// Find the most frequent communication pairs (from data exploration)
MATCH (p1:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(p2:Person)
WHERE p1.name < p2.name  // Avoid duplicates
WITH p1.name as person1, p2.name as person2, count(DISTINCT s) as shared_sessions,
     collect(DISTINCT s.sessiontype) as communication_types
WHERE shared_sessions >= 3
RETURN person1, person2, shared_sessions, communication_types,
       size(communication_types) as method_diversity
ORDER BY shared_sessions DESC
LIMIT 20;

// =============================================================================
// 30. NETWORK CONNECTIVITY ANALYSIS
// =============================================================================
// Find the most connected people by unique contacts (from data exploration)
MATCH (person:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(contact:Person)
WHERE person <> contact
WITH person, count(DISTINCT contact) as unique_contacts,
     count(DISTINCT s) as total_sessions
WHERE unique_contacts >= 5
RETURN person.name as person_name,
       unique_contacts,
       total_sessions,
       round(1.0 * total_sessions / unique_contacts, 1) as avg_sessions_per_contact
ORDER BY unique_contacts DESC;
// Whiskey Jack Dataset Results: ziezieken88@gmail.com & Kenzie Hawk (16 contacts), Richard Eagle (11 contacts), William Eagle (8 contacts)

// =============================================================================
// 31. TEMPORAL COMMUNICATION PATTERNS
// =============================================================================
// Analyze communication patterns by hour of day (from data exploration)
MATCH (s:Session)
WHERE s.starttime IS NOT NULL
WITH s, time(s.starttime).hour as hour_of_day
RETURN hour_of_day,
       count(*) as session_count,
       count(CASE WHEN s.sessiontype = 'Telephony' THEN 1 ELSE null END) as call_count,
       count(CASE WHEN s.sessiontype = 'Messaging' THEN 1 ELSE null END) as message_count,
       count(CASE WHEN s.sessiontype = 'Email' THEN 1 ELSE null END) as email_count
ORDER BY hour_of_day;
// Whiskey Jack Dataset Results: Peak activity at 14:00 (37 sessions), 19:00 (35 sessions), 18:00 (29 sessions)

// =============================================================================
// 32. DEVICE-TO-PHONE CORRELATION
// =============================================================================
// Map devices to their phone numbers and owners (from data exploration)
MATCH (device:Device)-[:HAS_ACCOUNT]->(phone:Phone)
OPTIONAL MATCH (person:Person)-[:USES_DEVICE]->(device)
OPTIONAL MATCH (phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN device.imei as device_imei,
       collect(DISTINCT phone.number) as phone_numbers,
       collect(DISTINCT person.name) as device_owners,
       count(DISTINCT s) as total_sessions
ORDER BY total_sessions DESC;

// =============================================================================
// 33. CONTENT TYPE DISTRIBUTION ANALYSIS
// =============================================================================
// Analyze the types of content in communications (from data exploration)
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.contentType IS NOT NULL
WITH count(*) as total_content_items
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.contentType IS NOT NULL
WITH c.contentType as content_type, count(*) as content_count,
     count(DISTINCT s) as sessions_with_this_type, total_content_items
RETURN content_type, content_count, sessions_with_this_type,
       round(100.0 * content_count / total_content_items, 1) as percentage
ORDER BY content_count DESC;
// Whiskey Jack Dataset Results: text/html 46.5%, text/plain 24.7%, audio/x-wav 19.5%, others <10%

// =============================================================================
// 34. MULTI-CONTENT SESSION ANALYSIS
// =============================================================================
// Find sessions with multiple content items (from data exploration)
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WITH s, count(c) as content_count, collect(c.contentType) as content_types
WHERE content_count > 1
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid as session_id,
       s.sessiontype as session_type,
       content_count,
       content_types,
       collect(DISTINCT p.name) as participants
ORDER BY content_count DESC
LIMIT 15;
// Whiskey Jack Dataset Results: Found 37 sessions with multiple content items, mostly emails with HTML/plain text + images

// =============================================================================
// 35. DATA QUALITY: SESSIONS WITHOUT CONTENT
// =============================================================================
// Find sessions that have no content (data quality check)
MATCH (s:Session)
WHERE NOT (s)-[:HAS_CONTENT]->()
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid as session_id,
       s.sessiontype as session_type,
       s.starttime as start_time,
       collect(DISTINCT p.name) as participants,
       'NO_CONTENT' as issue_type
ORDER BY s.starttime DESC
LIMIT 20;

// =============================================================================
// 36. VECTOR EMBEDDING STATUS CHECK
// =============================================================================
// Check which content has embeddings for semantic search (from vector search verification)
MATCH (c:Content)
RETURN count(CASE WHEN c.embedding IS NOT NULL THEN 1 END) as content_with_embeddings,
       count(CASE WHEN c.embedding IS NULL THEN 1 END) as content_without_embeddings,
       count(*) as total_content,
       round(100.0 * count(CASE WHEN c.embedding IS NOT NULL THEN 1 END) / count(*), 1) as embedding_coverage_percent;

// =============================================================================
// 37. ADVANCED SEMANTIC CONTENT SIMILARITY
// =============================================================================
// Find content similar to a specific piece using vector embeddings (from vector search verification)
// This finds content similar to the first available embedded content
MATCH (c:Content)
WHERE c.embedding IS NOT NULL
WITH c.embedding as query_vector, c.text as reference_text
LIMIT 1
CALL db.index.vector.queryNodes('ContentVectorIndex', 10, query_vector) 
YIELD node, score
WHERE score > 0.7  // Only high similarity matches
MATCH (s:Session)-[:HAS_CONTENT]->(node)
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN reference_text[0..100] + '...' as reference_content,
       node.id as similar_content_id,
       score as similarity_score,
       substring(node.text, 0, 200) as similar_content_preview,
       collect(DISTINCT p.name) as participants_in_similar_content
ORDER BY similarity_score DESC;

// =============================================================================
// 38. CROSS-CONTENT SIMILARITY ANALYSIS
// =============================================================================
// Analyze similarity patterns across all embedded content (from vector search verification)
MATCH (c1:Content)
WHERE c1.embedding IS NOT NULL
WITH collect({id: c1.id, embedding: c1.embedding, text: substring(c1.text, 0, 50)}) as content_items
UNWIND content_items as content1
CALL db.index.vector.queryNodes('ContentVectorIndex', 3, content1.embedding) 
YIELD node as content2, score
WHERE content1.id <> content2.id AND score > 0.8  // High similarity threshold
RETURN content1.id as content1_id,
       content1.text as content1_preview,
       content2.id as content2_id, 
       substring(content2.text, 0, 50) as content2_preview,
       score as similarity_score
ORDER BY similarity_score DESC
LIMIT 20;

// =============================================================================
// 39. EMBEDDED CONTENT WITH SESSION CONTEXT
// =============================================================================
// View embedded content with their associated session information (from vector search verification)
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.embedding IS NOT NULL
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid as session_id,
       s.sessiontype as session_type,
       s.starttime as session_time,
       collect(DISTINCT p.name) as participants,
       c.id as content_id,
       size(c.embedding) as embedding_dimensions,
       substring(c.text, 0, 200) as content_preview
ORDER BY s.starttime DESC
LIMIT 25;

// =============================================================================
// IMPORTANT NOTES FOR INVESTIGATORS
// =============================================================================
// 
// DATA QUALITY ISSUES THAT MAY AFFECT QUERIES:
// - Some temporal queries return no results if starttime field is null
// - Note: sessiondate is a computed field that will be added during import
// - Content type analysis may show null if contentType field not populated  
// - Vector similarity requires embeddings to be generated first (run generate-embeddings.sh)
// - Communication pattern changes need data spanning the cutoff date
//
// PROVEN WORKING QUERIES IN WHISKEY JACK DATASET:
// - Queries 4, 8, 9, 14, 17, 18, 20, 22, 30, 31, 33, 34: Consistently return useful investigative results
// - Full-text search (Query 17) and semantic search (Query 18) are particularly powerful
// - Network analysis queries (22, 30) reveal communication hubs and relationships
//
// CUSTOMIZATION TIPS:
// - Replace person names, phone numbers, dates with your investigation targets
// - Adjust thresholds (session counts, percentages) based on your dataset size
// - Modify keywords in content searches for your specific case

// End of practical investigation queries