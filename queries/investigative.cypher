// =============================================================================
// SPECIFIC CASE INVESTIGATION QUERIES
// =============================================================================
// These queries demonstrate specific surveillance investigations using real data

// 1. Top 3 associates of Kenzie Hawk
RETURN '--- 1. Top 3 associates of Kenzie Hawk ---' AS step;
MATCH (:Person {name:'@Kenzie Hawk'})-[:USES]->()-[:PARTICIPATED_IN]->(s)<-[:PARTICIPATED_IN]-()-[:USES]->(acct)<-[:USES]-(assoc:Person)
WHERE assoc.name <> '@Kenzie Hawk'
RETURN assoc.name AS Associate, count(DISTINCT s) AS Interactions
ORDER BY Interactions DESC LIMIT 3;
// Results: @jadog83@gmail.com (1 interaction)

// 2. IMEIs associated with phone 9366351931
RETURN '--- 2. IMEIs associated with phone 9366351931 ---' AS step;
MATCH (ph:Phone {number:'9366351931'})<-[:HAS_ACCOUNT]-(d:Device)
RETURN d.imei, COUNT { (d)-[:HAS_ACCOUNT]->(:Phone)-[:PARTICIPATED_IN]->() } AS totalSessions;
// Results: IMEI 359847107165930 (90 sessions), IMEI 861616045977978 (154 sessions)

// 3. William Eagle's communication profile analysis
RETURN '--- 3. William Eagle Communication Profile ---' AS step;
MATCH (william:Person {name: '@Eagle, William'})-[:USES]->(method)
RETURN labels(method)[0] as communication_method,
       COALESCE(method.number, method.email) as identifier,
       COUNT { (method)-[:PARTICIPATED_IN]->() } as sessions
ORDER BY sessions DESC;
// Results: Phone 9366351931 (75 sessions), Phone 9364254000 (5 sessions)

// 4. Kenzie Hawk device and phone correlation
RETURN '--- 4. Kenzie Device Analysis ---' AS step;
MATCH (kenzie:Person)-[:USES_DEVICE]->(d:Device)-[:HAS_ACCOUNT]->(ph:Phone)
WHERE kenzie.name CONTAINS 'Kenzie'
RETURN d.imei as device_imei,
       ph.number as phone_number,
       COUNT { (ph)-[:PARTICIPATED_IN]->() } as phone_sessions
ORDER BY phone_sessions DESC;
// Results: IMEI 358798097379882 → Phone 3032663434 (91 sessions)
//          IMEI 358642101048957 → Phone 3032663434 (91 sessions), Phone 3035950505 (2 sessions)

// 5. Email relationship mapping - Kenzie to jadog83
RETURN '--- 5. Kenzie-jadog83 Email Investigation ---' AS step;
MATCH (kenzie_email:Email {email: 'ziezieken88@gmail.com'})-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(other_email:Email {email: 'jadog83@gmail.com'})
OPTIONAL MATCH (s)-[:HAS_CONTENT]->(c:Content)
RETURN count(DISTINCT s) as email_exchanges,
       min(s.starttime) as first_contact,
       max(s.starttime) as last_contact,
       [content IN collect(substring(c.text, 0, 100)) WHERE content IS NOT NULL][0..2] as content_samples;
// Results: 22 email exchanges, First contact: 2000-04-03, Last contact: 2022-02-04
//          Content samples: "Subject: Drinks\nLocation: You know the place" (calendar event)
