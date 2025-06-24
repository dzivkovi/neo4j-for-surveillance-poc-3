// Comprehensive Validation Suite for Implemented Evaluations
// Tests confirmed working as of June 24, 2025
// Usage: docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < evals/validation-queries/test-implemented.cypher

// EVAL-06: Has Kenzie referenced a shed?
CALL db.index.fulltext.queryNodes('ContentFullText', 'shed') YIELD node, score
MATCH (s:Session)-[:HAS_CONTENT]->(node)
RETURN 'EVAL-06' as test_id,
       count(*) as shed_mentions,
       max(score) as best_match_score;

// EVAL-08: Are there any references to sago palms?
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago palms') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN 'EVAL-08' as test_id,
       count(*) as mention_count,
       avg(score) as avg_relevance;

// EVAL-23: How many pertinent sessions are there?
MATCH (s:Session)
WHERE s.classification = 'Pertinent'
RETURN 'EVAL-23' as test_id,
       count(s) as pertinent_sessions;

// EVAL-25: How many sessions are still under review?
MATCH (s:Session)
WHERE s.reviewstatus = 'In Process'
RETURN 'EVAL-25' as test_id,
       count(s) as sessions_under_review;

// EVAL-26: How many telephony sessions are there?
MATCH (s:Session)
WHERE s.sessiontype = 'Telephony'
RETURN 'EVAL-26' as test_id,
       count(s) as telephony_sessions;

// EVAL-27: How many sessions contain audio?
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.contentType STARTS WITH 'audio/'
RETURN 'EVAL-27' as test_id,
       count(DISTINCT s) as audio_sessions;

// EVAL-29: How many telephony sessions are longer than a minute?
MATCH (s:Session)
WHERE s.sessiontype = 'Telephony' 
  AND s.durationinseconds > 60
RETURN 'EVAL-29' as test_id,
       count(*) as long_calls,
       avg(s.durationinseconds) as avg_duration_seconds;

// EVAL-34: How does Kenzie communicate with Owen?
MATCH (k:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(o:Person)
WHERE k.name CONTAINS 'Kenzie' AND o.name CONTAINS 'Owen'
RETURN 'EVAL-34' as test_id,
       s.sessiontype as communication_type,
       count(*) as count
ORDER BY count DESC;

// EVAL-43: Who are William Eagle's top associates?
MATCH (w:Person {name:'@Eagle, William'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(assoc:Person)
WHERE assoc.name <> '@Eagle, William'
RETURN 'EVAL-43' as test_id,
       assoc.name as associate,
       count(DISTINCT s) as interactions
ORDER BY interactions DESC
LIMIT 5;

// EVAL-68: What phone numbers is Kenzie using?
CALL db.index.fulltext.queryNodes('AliasText', 'Kenzie') 
YIELD node
MATCH (node)-[:ALIAS_OF]->(p:Person)<-[:ALIAS_OF]-(phone:Alias {type: 'msisdn'})
RETURN 'EVAL-68' as test_id, 
       count(DISTINCT phone.rawValue) as phone_count,
       collect(DISTINCT phone.rawValue)[0..3] as sample_phones;

// EVAL-70: What are Kenzie's IMEIs?
MATCH (k:Person)-[:USES_DEVICE]->(d:Device)
WHERE k.name CONTAINS 'Kenzie'
RETURN 'EVAL-70' as test_id,
       collect(d.imei) as kenzie_imeis,
       count(d.imei) as imei_count;

// EVAL-71: Which IMEIs are associated with phone 9366351931?
MATCH (ph:Phone {number:'9366351931'})<-[:HAS_ACCOUNT]-(d:Device)
RETURN 'EVAL-71' as test_id,
       collect(d.imei) as associated_imeis,
       count(d.imei) as imei_count;

// EVAL-73: Who has been using devices with IMEI 359847107165930?
MATCH (d:Device {imei:'359847107165930'})<-[:USES_DEVICE]-(p:Person)
RETURN 'EVAL-73' as test_id,
       collect(p.name) as device_users,
       count(p.name) as user_count;

// EVAL-75: What is Kenzie Hawk's email address?
MATCH (k:Person)-[:USES]->(e:Email)
WHERE k.name CONTAINS 'Kenzie'
RETURN 'EVAL-75' as test_id,
       e.email as kenzie_email;

// EVAL-01: Does fred discuss travel plans?
CALL db.index.fulltext.queryNodes('ContentFullText', 'Fred travel plans departure leaving Miami Mobile') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
OPTIONAL MATCH (s)<-[:PARTICIPATED_IN]-()<-[:USES]-(p:Person)
WHERE p.name CONTAINS 'Fred' OR p.name CONTAINS 'Merlin'
RETURN 'EVAL-01' as test_id,
       count(*) as travel_discussions,
       max(score) as best_match_score;

// EVAL-15: Are any of the following included: cherry blasters, BMWs, tracking devices
WITH ['cherry blasters', 'BMWs', 'tracking devices'] AS search_terms
UNWIND search_terms AS term
CALL db.index.fulltext.queryNodes('ContentFullText', term) 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN 'EVAL-15' as test_id, term, count(*) as mentions, max(score) as best_score
ORDER BY mentions DESC;

// EVAL-24: How many recent pertinent sessions are there? (Feb 14-15)
MATCH (s:Session)
WHERE s.classification = 'Pertinent'
  AND date(datetime(s.starttime)) >= date('2020-02-14')
  AND date(datetime(s.starttime)) <= date('2020-02-15')
RETURN 'EVAL-24' as test_id,
       count(*) as recent_pertinent_sessions;

// EVAL-28: How many sessions contain audio between Feb 14-15 2020?
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.contentType STARTS WITH 'audio/'
  AND date(datetime(s.starttime)) >= date('2020-02-14')
  AND date(datetime(s.starttime)) <= date('2020-02-15')
RETURN 'EVAL-28' as test_id,
       count(DISTINCT s) as audio_sessions_feb14_15;

// EVAL-31: What are the top applications used in this case?
MATCH (s:Session)
WHERE s.sessiontype IS NOT NULL
RETURN 'EVAL-31' as test_id,
       s.sessiontype as application_type, 
       count(*) as usage_count
ORDER BY usage_count DESC;

// EVAL-32: What applications do Kenzie and Owen use to communicate?
MATCH (k:Person {name: '@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(o:Person {name: '@Frasier, Owen'})
RETURN 'EVAL-32' as test_id,
       s.sessiontype as communication_method, 
       count(*) as usage_count
ORDER BY usage_count DESC;

// EVAL-33: What types of applications are used by Kenzie?
MATCH (k:Person {name: '@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)
RETURN 'EVAL-33' as test_id,
       s.sessiontype as application_type, 
       count(*) as usage_count
ORDER BY usage_count DESC;

// EVAL-41: How do Kenzie and William communicate?
MATCH (k:Person {name: '@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(w:Person {name: '@Eagle, William'})
RETURN 'EVAL-41' as test_id,
       s.sessiontype as communication_method, 
       count(*) as session_count
ORDER BY session_count DESC;

// EVAL-42: when does Kenzie normally talk with William?
MATCH (k:Person {name: '@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(w:Person {name: '@Eagle, William'})
WITH s, datetime(s.starttime) as dt
RETURN 'EVAL-42' as test_id,
       dt.dayOfWeek as day_of_week,
       date(dt) as communication_date,
       count(*) as sessions_on_date
ORDER BY communication_date;

// EVAL-44: Who does Martha interact with most?
MATCH (martha:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(other:Person)
WHERE martha.name CONTAINS 'Martha' AND other.name <> martha.name
RETURN 'EVAL-44' as test_id,
       other.name as person, 
       count(DISTINCT s) as interactions
ORDER BY interactions DESC
LIMIT 5;

// EVAL-45: Who are Kenzie's top 3 associates?
MATCH (k:Person {name: '@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(assoc:Person)
WHERE assoc.name <> '@Hawk, Kenzie'
RETURN 'EVAL-45' as test_id,
       assoc.name as associate, 
       count(DISTINCT s) as activities
ORDER BY activities DESC
LIMIT 3;

// EVAL-36: Summarize Owen's communications (with critical compliance verification)
MATCH (owen:Person {name: '@Frasier, Owen'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(other:Person)
WHERE other.name <> '@Frasier, Owen'
RETURN 'EVAL-36' as test_id,
       other.name as communication_partner, 
       count(DISTINCT s) as sessions,
       collect(DISTINCT s.sessiontype) as communication_types
ORDER BY sessions DESC;

// EVAL-38: Owen's latest activities (Feb 14-15)
MATCH (owen:Person {name: '@Frasier, Owen'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)
WHERE date(datetime(s.starttime)) >= date('2020-02-14')
  AND date(datetime(s.starttime)) <= date('2020-02-15')
RETURN 'EVAL-38' as test_id,
       count(DISTINCT s) as latest_sessions,
       collect(DISTINCT date(datetime(s.starttime))) as activity_dates;

// EVAL-39: When does Mildred communicate with Kenzie?
MATCH (mildred:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(kenzie:Person)
WHERE mildred.name CONTAINS 'Mildred' AND kenzie.name CONTAINS 'Kenzie'
WITH s, datetime(s.starttime) as session_time
RETURN 'EVAL-39' as test_id,
       date(session_time) as communication_date,
       session_time.hour as hour_of_day,
       count(*) as sessions_that_day
ORDER BY communication_date;

// EVAL-40: When does <@Mildred> communicate with <@Hawk, Kenzie>?
MATCH (mildred:Person {name: '@Mildred'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(kenzie:Person {name: '@Hawk, Kenzie'})
WITH s, datetime(s.starttime) as session_time
RETURN 'EVAL-40' as test_id,
       date(session_time) as date_communicated,
       session_time.hour as hour,
       s.sessiontype as method,
       count(*) as sessions
ORDER BY date_communicated, hour;

// EVAL-46: Richard's communications on February 6, 2020
MATCH (richard:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)
WHERE richard.name CONTAINS 'Richard' 
  AND date(datetime(s.starttime)) = date('2020-02-06')
RETURN 'EVAL-46' as test_id,
       richard.name as person,
       count(DISTINCT s) as sessions_feb_6,
       collect(DISTINCT s.sessiontype) as communication_types;

// EVAL-47: Major topics analysis
WITH ['meeting', 'travel', 'property', 'landscaping', 'equipment', 'shed', 'pricing', 'payment'] as topics
UNWIND topics as topic
CALL db.index.fulltext.queryNodes('ContentFullText', topic) 
YIELD node, score
WHERE score > 1.0
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN 'EVAL-47' as test_id,
       topic, 
       count(DISTINCT s) as sessions_mentioning_topic
ORDER BY sessions_mentioning_topic DESC
LIMIT 8;

// EVAL-66: Kenzie's most recent location
MATCH (k:Person {name: '@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)-[:LOCATED_AT]->(l:Location)
WITH s, l, datetime(s.starttime) as session_time
ORDER BY session_time DESC
RETURN 'EVAL-66' as test_id,
       l.geo as most_recent_location,
       session_time as timestamp
LIMIT 1;

// EVAL-69: William's phone numbers with usage frequency
MATCH (william:Person {name: '@Eagle, William'})-[:USES]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN 'EVAL-69' as test_id,
       phone.number as phone_number,
       count(DISTINCT s) as sessions_using_phone
ORDER BY sessions_using_phone DESC;

// EVAL-72: Phone numbers associated with IMEI 359847107165930
MATCH (device:Device {imei: '359847107165930'})-[:HAS_ACCOUNT]->(phone:Phone)
RETURN 'EVAL-72' as test_id,
       collect(phone.number) as associated_phones,
       count(phone.number) as phone_count;

// EVAL-74: IMEI 352897117153653 details
MATCH (device:Device {imei: '352897117153653'})
OPTIONAL MATCH (device)-[:HAS_ACCOUNT]->(phone:Phone)
OPTIONAL MATCH (device)<-[:USES_DEVICE]-(person:Person)
OPTIONAL MATCH (phone)-[:PARTICIPATED_IN]->(session:Session)
RETURN 'EVAL-74' as test_id,
       device.imei as imei,
       collect(DISTINCT phone.number) as phone_numbers,
       collect(DISTINCT person.name) as users,
       count(DISTINCT session) as sessions_count;

// EVAL-76: Kenzie's email exchanges with jadog83@gmail.com
MATCH (kenzie_email:Email {email: 'ziezieken88@gmail.com'})-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(jadog_email:Email {email: 'jadog83@gmail.com'})
RETURN 'EVAL-76' as test_id,
       count(DISTINCT s) as email_exchanges;

// EVAL-77: All email addresses that ziezieken88@gmail.com interacts with
MATCH (kenzie_email:Email {email: 'ziezieken88@gmail.com'})-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(other_email:Email)
WHERE other_email.email <> 'ziezieken88@gmail.com'
RETURN 'EVAL-77' as test_id,
       other_email.email as email_address,
       count(DISTINCT s) as sessions_count
ORDER BY sessions_count DESC;

// SUMMARY: Overall Implementation Status
MATCH (s:Session)
OPTIONAL MATCH (s)-[:HAS_CONTENT]->(c:Content)
OPTIONAL MATCH (a:Alias)
RETURN 'SUMMARY' as test_id,
       count(DISTINCT s) as total_sessions,
       count(DISTINCT c) as total_content_nodes,
       count(DISTINCT a) as total_aliases,
       count(DISTINCT CASE WHEN a.type = 'msisdn' THEN a END) as phone_aliases,
       count(DISTINCT CASE WHEN s.sessiontype = 'Telephony' THEN s END) as telephony_sessions;