// 1. Top 3 associates of Kenzie Hawk
RETURN '--- 1. Top 3 associates of Kenzie Hawk ---' AS step;
MATCH (:Person {name:'@Kenzie Hawk'})-[:USES]->()-[:PARTICIPATED_IN]->(s)<-[:PARTICIPATED_IN]-()-[:USES]->(acct)<-[:USES]-(assoc:Person)
WHERE assoc.name <> '@Kenzie Hawk'
RETURN assoc.name AS Associate, count(DISTINCT s) AS Interactions
ORDER BY Interactions DESC LIMIT 3;

// 2. IMEIs associated with phone 9366351931
RETURN '--- 2. IMEIs associated with phone 9366351931 ---' AS step;
MATCH (ph:Phone {number:'9366351931'})<-[:HAS_ACCOUNT]-(d:Device)
RETURN d.imei, COUNT { (d)-[:HAS_ACCOUNT]->(:Phone)-[:PARTICIPATED_IN]->() } AS totalSessions;
