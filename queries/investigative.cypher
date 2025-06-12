// Top 3 associates of Kenzie Hawk
MATCH (:Person {name:'Kenzie Hawk'})-[:USES]->()-[:PARTICIPATED_IN]->(s)<-[:PARTICIPATED_IN]-()-[:USES]->(acct)<-[:USES]-(assoc:Person)
WHERE assoc.name <> 'Kenzie Hawk'
RETURN assoc.name AS Associate, count(DISTINCT s) AS Interactions
ORDER BY Interactions DESC LIMIT 3;

// Does Fred discuss travel plans?
WITH 'Fred Merlin' AS target
MATCH (p:Person {name:target})-[:USES]->()-[:PARTICIPATED_IN]->(s)-[:HAS_CONTENT]->(c)
CALL db.index.vector.queryNodes('ContentVectorIndex',
  $travelPlansVector, 10) YIELD node, score
WHERE node = c
RETURN p.name, s.sessionguid, score, c.text
ORDER BY score DESC;

// IMEIs associated with phone 9366351931
MATCH (ph:Phone {number:'9366351931'})<-[:HAS_ACCOUNT]-(d:Device)
RETURN d.imei, size( (d)-[:HAS_ACCOUNT]->(:Phone)-[:PARTICIPATED_IN]->() ) AS totalSessions;
