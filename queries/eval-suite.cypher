/***************************************************************************
  EVALUATION SUITE - Neo4j Surveillance PoC
  ==========================================
  Purpose: Validate that the imported surveillance graph meets business
           acceptance criteria from evaluation_tests.md
  
  Usage: cypher-shell -u neo4j -p Sup3rSecur3! -f queries/eval-suite.cypher
  
  This file tests the core business questions that law enforcement
  investigators need to answer using the surveillance data.
***************************************************************************/

/*-------------------------------------------------------------------------
 SECTION A: SCHEMA VALIDATION
-------------------------------------------------------------------------*/
RETURN '=== SECTION A: SCHEMA VALIDATION ===' AS header;

// A-1: Verify all required constraints exist
RETURN '--- A-1: Checking Constraints ---' AS step;
SHOW CONSTRAINTS;
/* Expected: session_guid, phone_number, email_addr, device_imei */

// A-2: Verify all indexes are ONLINE
RETURN '--- A-2: Checking Indexes ---' AS step;
SHOW INDEXES
YIELD name, type, state, populationPercent, entityType, labelsOrTypes, properties
ORDER BY type, name;
/* Look for: ContentFullText (FULLTEXT), ContentVectorIndex (VECTOR) */

// A-3: Ensure indexes are ready
CALL db.awaitIndexes();

/*-------------------------------------------------------------------------
 SECTION B: DATA SANITY CHECKS  
-------------------------------------------------------------------------*/
RETURN '=== SECTION B: DATA SANITY CHECKS ===' AS header;

// B-1: Node counts (should match import expectations)
RETURN '--- B-1: Node Counts ---' AS step;
MATCH (n)
RETURN labels(n)[0] AS NodeType, count(*) AS Count
ORDER BY Count DESC;
/* Expected: ~265 Sessions, ~40 Persons, ~24 Phones, ~18 Emails, ~17 Devices, ~215 Content */

// B-2: Session breakdown by type
RETURN '--- B-2: Session breakdown by type ---' AS step;
MATCH (s:Session)
RETURN s.sessiontype AS SessionType, count(*) AS Count
ORDER BY Count DESC;

// B-3: Content nodes with embeddings
RETURN '--- B-3: Content nodes with embeddings ---' AS step;
MATCH (c:Content)
RETURN 
  count(CASE WHEN c.embedding IS NOT NULL THEN 1 END) AS WithEmbeddings,
  count(CASE WHEN c.embedding IS NULL THEN 1 END) AS WithoutEmbeddings,
  count(*) AS TotalContent;

/*-------------------------------------------------------------------------
 SECTION C: CORE BUSINESS QUERIES (from evaluation_tests.md)
-------------------------------------------------------------------------*/
RETURN '=== SECTION C: CORE BUSINESS QUERIES ===' AS header;

// C-1: "Who are William Eagle's top associates?" (EVAL-43)
RETURN '--- C-1: William Eagle Associates ---' AS step;
MATCH (w:Person {name:'@Eagle, William'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(assoc:Person)
WHERE assoc.name <> '@Eagle, William'
RETURN assoc.name AS Associate, count(DISTINCT s) AS Interactions
ORDER BY Interactions DESC
LIMIT 5;
/* Expected: Richard Eagle (top), Fred Merlin, Kenzie Hawk, etc. */

// C-2: "What are Kenzie's IMEIs?" (EVAL-70)
RETURN '--- C-2: Kenzie IMEIs ---' AS step;
MATCH (k:Person)-[:USES_DEVICE]->(d:Device)
WHERE k.name CONTAINS 'Kenzie'
OPTIONAL MATCH (d)-[:HAS_ACCOUNT]->(ph:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN d.imei AS IMEI, count(DISTINCT s) AS SessionCount
ORDER BY SessionCount DESC;
/* Expected: Two IMEIs with different session counts */

// C-3: "Which IMEIs are associated with phone 9366351931?" (EVAL-71)
RETURN '--- C-3: IMEIs are associated with phone 9366351931 ---' AS step;
MATCH (ph:Phone {number:'9366351931'})<-[:HAS_ACCOUNT]-(d:Device)
RETURN d.imei AS IMEI;
/* Expected: Multiple IMEIs for this phone number */

// C-4: "What is Kenzie Hawk's email address?" (EVAL-75)
RETURN '--- C-4: Kenzie email addresses ---' AS step;
MATCH (k:Person)-[:USES]->(e:Email)
WHERE k.name CONTAINS 'Kenzie'
RETURN e.email AS EmailAddress;
/* Expected: ziezieken88@gmail.com */

// C-5: "Who has been using devices with IMEI 359847107165930?" (EVAL-73)
RETURN '--- C-5: IMEI 359847107165930 users ---' AS step;
MATCH (d:Device {imei:'359847107165930'})<-[:USES_DEVICE]-(p:Person)
OPTIONAL MATCH (d)-[:HAS_ACCOUNT]->(ph:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN p.name AS Person, count(DISTINCT s) AS SessionCount
ORDER BY SessionCount DESC;
/* Expected: William Eagle (high count), possibly Ted Dowitcher */

// C-6: "How does Kenzie communicate with Owen?" (EVAL-34)
RETURN '--- C-6: How does Kenzie communicate with Owen ---' AS step;
MATCH (k:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(o:Person)
WHERE k.name CONTAINS 'Kenzie' AND o.name CONTAINS 'Owen'
RETURN s.sessiontype AS CommunicationType, count(*) AS Count
ORDER BY Count DESC;
/* Expected: SMS/messaging and telephony sessions */

/*-------------------------------------------------------------------------
 SECTION D: CONTENT SEARCH VALIDATION
-------------------------------------------------------------------------*/
RETURN '=== SECTION D: CONTENT SEARCH VALIDATION ===' AS header;

// D-1: Full-text search for "shed" (EVAL-6,7)
RETURN '--- D-1: Full-text search for "shed" ---' AS step;
CALL db.index.fulltext.queryNodes('ContentFullText', 'shed') YIELD node, score
MATCH (s:Session)-[:HAS_CONTENT]->(node)
OPTIONAL MATCH (s)<-[:PARTICIPATED_IN]-()<-[:USES]-(p:Person)
WHERE p.name CONTAINS 'Kenzie'
RETURN s.sessionguid AS SessionGUID, score, substring(node.text, 0, 100) AS ContentPreview
ORDER BY score DESC
LIMIT 5;

// D-2: Full-text search for "sago palms" (EVAL-8,9,10)
RETURN '--- D-2: Full-text search for "sago palms" ---' AS step;
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago OR palms') YIELD node, score
MATCH (s:Session)-[:HAS_CONTENT]->(node)
RETURN s.sessionguid AS SessionGUID, s.starttime AS DateTime, score, 
       substring(node.text, 0, 120) AS ContentPreview
ORDER BY score DESC
LIMIT 10;

// D-3: Vector similarity test (requires embedding parameter)
// Note: This query needs a pre-computed vector for "travel plans"
// MATCH (c:Content) WHERE c.embedding IS NOT NULL 
// WITH c.embedding AS sampleVector LIMIT 1
// CALL db.index.vector.queryNodes('ContentVectorIndex', 5, sampleVector) 
// YIELD node, score
// RETURN node.id AS ContentID, score, substring(node.text, 0, 100) AS Preview
// ORDER BY score DESC;

/*-------------------------------------------------------------------------
 SECTION E: TIME AND METADATA FILTERING  
-------------------------------------------------------------------------*/
RETURN '=== SECTION E: TIME AND METADATA FILTERING ===' AS header;

// E-1: Morning sessions count (EVAL-20)
RETURN '--- E-1: Morning sessions count ---' AS step;
MATCH (s:Session)
WHERE s.createddate.hour >= 8 AND s.createddate.hour <= 10
RETURN count(s) AS MorningSessions;
/* Expected: ~44 sessions */

// E-2: Pertinent sessions (EVAL-23)
RETURN '--- E-2: Pertinent sessions ---' AS step;
MATCH (s:Session)
WHERE s.classification = 'Pertinent'
RETURN count(s) AS PertinentSessions;

// E-3: Telephony sessions (EVAL-26)
RETURN '--- E-3: Telephony sessions ---' AS step;
MATCH (s:Session)
WHERE s.sessiontype = 'Telephony'
RETURN count(s) AS TelephonySessions;

// E-4: Sessions with audio content (EVAL-27)
RETURN '--- E-4: Sessions with audio content ---' AS step;
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.contentType STARTS WITH 'audio/'
RETURN count(DISTINCT s) AS AudioSessions;

/*-------------------------------------------------------------------------
 SECTION F: RELATIONSHIP TRAVERSAL TESTS
-------------------------------------------------------------------------*/
RETURN '=== SECTION F: RELATIONSHIP TRAVERSAL TESTS ===' AS header;

// F-1: Person-to-Person communication paths
RETURN '--- F-1: Person-to-Person communication paths ---' AS step;
MATCH (p1:Person {name:'@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(p2:Person)
WHERE p1 <> p2
RETURN p2.name AS Contact, count(DISTINCT s) AS SharedSessions
ORDER BY SharedSessions DESC
LIMIT 10;

// F-2: Device usage patterns
RETURN '--- F-2: Device usage patterns ---' AS step;
MATCH (d:Device)-[:HAS_ACCOUNT]->(ph:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN d.imei AS IMEI, ph.number AS PhoneNumber, count(s) AS SessionCount
ORDER BY SessionCount DESC
LIMIT 10;

// F-3: Most active phone numbers
RETURN '--- F-3: Most active phone numbers ---' AS step;
MATCH (ph:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN ph.number AS PhoneNumber, count(s) AS SessionCount
ORDER BY SessionCount DESC
LIMIT 10;

/*-------------------------------------------------------------------------
 SECTION G: SEMANTIC SEARCH VALIDATION (Business Critical)
-------------------------------------------------------------------------*/
RETURN '=== SECTION G: SEMANTIC SEARCH VALIDATION ===' AS header;

// G-1: Find content about travel (text-based approach)
RETURN '--- G-1: Find content about travel (text-based approach) ---' AS step;
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE toLower(c.text) CONTAINS 'travel' 
   OR toLower(c.text) CONTAINS 'trip' 
   OR toLower(c.text) CONTAINS 'bangkok'
   OR toLower(c.text) CONTAINS 'flight'
RETURN s.sessionguid AS SessionGUID, s.targetname AS Target, s.subject AS Subject,
       substring(c.text, 0, 150) AS ContentPreview
LIMIT 10;

// G-2: Sessions by target person
RETURN '--- G-2: Sessions by target person ---' AS step;
MATCH (s:Session)
WHERE s.targetname IS NOT NULL
RETURN s.targetname AS Target, count(*) AS SessionCount
ORDER BY SessionCount DESC;

/*-------------------------------------------------------------------------
 SECTION H: DATA QUALITY CHECKS
-------------------------------------------------------------------------*/
RETURN '=== SECTION H: DATA QUALITY CHECKS ===' AS header;

// H-1: Sessions without content
RETURN '--- H-1: Sessions without content ---' AS step;
MATCH (s:Session)
WHERE NOT (s)-[:HAS_CONTENT]->()
RETURN count(s) AS SessionsWithoutContent;

// H-2: Orphaned phones (not used by anyone)
RETURN '--- H-2: Orphaned phones (not used by anyone) ---' AS step;
MATCH (ph:Phone)
WHERE NOT ()-[:USES]->(ph)
RETURN ph.number AS OrphanedPhone;

// H-3: People without communication methods
RETURN '--- H-3: People without communication methods ---' AS step;
MATCH (p:Person)
WHERE NOT (p)-[:USES]->()
RETURN p.name AS PersonWithoutComms;

// H-4: Content missing text but has embedding
RETURN '--- H-4: Content missing text but has embedding ---' AS step;
MATCH (c:Content)
WHERE c.embedding IS NOT NULL AND (c.text IS NULL OR c.text = '')
RETURN count(c) AS ContentMissingText;

/***************************************************************************
 END OF EVALUATION SUITE
 
 Expected Results Summary:
 - All constraints and indexes should be ONLINE
 - ~265 Sessions, ~40 Persons, ~24 Phones, ~17 Devices, ~215 Content
 - William Eagle's top associate should be Richard Eagle
 - Kenzie should have 2 IMEIs with different usage patterns
 - Phone 9366351931 should be associated with multiple IMEIs
 - Travel-related content should be found (Bangkok trip planning)
 - Morning sessions should be ~44
 - Semantic searches should return relevant surveillance content
***************************************************************************/
