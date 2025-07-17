// Entity Resolution Rules
// Apply after initial data load to resolve anon-unknown aliases to actual persons
// Usage: docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < entity-resolution-rules.cypher

// RULE 1: William Eagle uses phones 9366351931 and 9364254000
MATCH (william:Person {name: '@Eagle, William'})
MATCH (ph1:Phone {number: '9366351931'})
MATCH (ph2:Phone {number: '9364254000'}) 
MERGE (william)-[:USES]->(ph1)
MERGE (william)-[:USES]->(ph2);

// RULE 2: Kenzie Hawk uses phone 9037549877 and email ziezieken88@gmail.com
MATCH (kenzie:Person {name: '@Hawk, Kenzie'})
MATCH (ph:Phone {number: '9037549877'})
MATCH (e:Email {email: 'ziezieken88@gmail.com'})
MERGE (kenzie)-[:USES]->(ph)
MERGE (kenzie)-[:USES]->(e);

// RULE 3: Fred Merlin uses phone 9362340298
MATCH (fred:Person {name: '@Merlin, Fred'})
MATCH (ph:Phone {number: '9362340298'})
MERGE (fred)-[:USES]->(ph);

// RULE 4: Richard Eagle uses phone 9364250033
MATCH (richard:Person {name: '@Eagle, Richard'})
MATCH (ph:Phone {number: '9364250033'})
MERGE (richard)-[:USES]->(ph);

// RULE 5: Owen Frasier uses email Ovenfrasier1@comcast.net
MATCH (owen:Person {name: '@Frasier, Owen'})
MATCH (e:Email {email: 'Ovenfrasier1@comcast.net'})
MERGE (owen)-[:USES]->(e);

// RULE 6: Martha Hawk uses phone 9366320866
MATCH (martha:Person {name: '@Hawk, Martha'})
MATCH (ph:Phone {number: '9366320866'})
MERGE (martha)-[:USES]->(ph);

// RULE 7: Ted Dowitcher uses phone 9366363001
MATCH (ted:Person {name: '@Dowitcher, Ted'})
MATCH (ph:Phone {number: '9366363001'})
MERGE (ted)-[:USES]->(ph);

// RULE 8: Mildred uses phone 9364250061
MATCH (mildred:Person {name: '@Mildred'})
MATCH (ph:Phone {number: '9364250061'})
MERGE (mildred)-[:USES]->(ph);

// VERIFICATION: Show results after applying rules
MATCH (p:Person)-[:USES]->(device)
WHERE p.name <> 'anon-unknown'
RETURN p.name as person, 
       labels(device) as device_type,
       CASE 
         WHEN 'Phone' IN labels(device) THEN device.number
         WHEN 'Email' IN labels(device) THEN device.email
       END as identifier
ORDER BY person;