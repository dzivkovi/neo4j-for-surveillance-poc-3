// Essential Graph Visualization Queries for Surveillance Analytics
// ==============================================================
// Copy-paste ready queries for Neo4j Browser that demonstrate
// graph database superiority over traditional databases.

// ============================================================================
// QUERY 1: Network Influence Analysis (Communication Hubs)
// ============================================================================
// Answers: "Who are the key players in this network?"
// Why graphs excel: Variable-length path traversal (*1..6) would require
// complex recursive CTEs in SQL with exponential performance degradation.

MATCH (person:Person)
WHERE person.name IN ['@Frasier, Owen', '@Eagle, William', '@Hawk, Kenzie', '@Merlin, Fred']
WITH person
MATCH (person)-[:USES|PARTICIPATED_IN*1..6]-(reached:Person)
WHERE reached <> person AND reached.name STARTS WITH '@'
RETURN 
  person.name as communication_hub,
  COUNT(DISTINCT reached) as people_within_3_degrees
ORDER BY people_within_3_degrees DESC;

// Expected results:
// - Kenzie Hawk: 9 people (high influence)
// - William Eagle: 8 people (key broker)
// - Fred Merlin: 4 people (limited network)
// - Owen Frasier: 2 people (isolated)

// ============================================================================
// QUERY 2: Weighted Relationship Visualization 
// ============================================================================
// Answers: "How strong are the connections between key suspects?"
// Creates visual graph where line thickness = communication frequency
// Requires APOC for virtual relationships

MATCH (p1:Person)-[:USES]->(c1)-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(c2)<-[:USES]-(p2:Person)
WHERE p1.name IN ['@Eagle, Richard', '@Eagle, William', '@Merlin, Fred', '@Ray']
  AND p2.name IN ['@Eagle, Richard', '@Eagle, William', '@Merlin, Fred', '@Ray']
  AND p1.name < p2.name
WITH p1, p2, COUNT(DISTINCT s) as strength
WHERE strength > 0
CALL apoc.create.vRelationship(p1, 'COMMUNICATES', {strength: strength, weight: strength}, p2) YIELD rel
RETURN p1, rel, p2;

// After running in Neo4j Browser:
// 1. Click "COMMUNICATES" in right sidebar under "Relationship types"
// 2. Select "strength" to show numbers on relationship lines
// 3. Line thickness will vary: thick (29 sessions) to thin (1 session)

// ============================================================================
// QUERY 3: Hidden Connection Discovery (Shortest Path)
// ============================================================================
// Answers: "How are these two people connected if they never directly communicate?"
// Reveals investigation leads through intermediaries

MATCH (person1:Person {name: '@Eagle, Beverly'}), (person2:Person {name: '@Ray'})
MATCH path = shortestPath((person1)-[:USES|PARTICIPATED_IN*..10]-(person2))
RETURN path;

// Shows Beverly Eagle connected to Ray through 6 hops via shared phones/sessions
// In SQL: Would require 6+ JOINs with exponential complexity

// ============================================================================
// BONUS: Communication Timeline for Specific Date
// ============================================================================
// Shows all communications on a specific day for timeline analysis

MATCH (s:Session)
WHERE date(s.starttime) = date('2020-02-06')
MATCH (p1:Person)-[:USES]->(c1)-[:PARTICIPATED_IN]->(s)<-[:PARTICIPATED_IN]-(c2)<-[:USES]-(p2:Person)
WHERE p1 <> p2
RETURN p1, p2, s, c1, c2
LIMIT 50;

// Reveals daily communication patterns and active participants
// Essential for establishing timelines in investigations