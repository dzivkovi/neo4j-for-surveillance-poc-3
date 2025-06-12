/*
  Neo4j Surveillance PoC - Data Exploration Queries
  =================================================
  Purpose: Interactive queries to explore and understand the surveillance data
  
  Usage: Run these queries in Neo4j Browser to explore your data
*/

// ============================================
// SECTION 1: Overview Statistics
// ============================================

// Count all node types with a single query
MATCH (n)
RETURN labels(n)[0] as NodeType, count(n) as Count
ORDER BY Count DESC;

// ============================================
// SECTION 2: Communication Patterns
// ============================================

// Who communicates the most? (Top 10 most active people)
MATCH (p:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)
RETURN p.name as Person, count(DISTINCT s) as SessionCount
ORDER BY SessionCount DESC
LIMIT 10;

// Session types breakdown
MATCH (s:Session)
RETURN s.sessiontype as Type, count(*) as Count
ORDER BY Count DESC;

// Sessions by classification
MATCH (s:Session)
RETURN s.classification as Classification, count(*) as Count
ORDER BY Count DESC;

// ============================================
// SECTION 3: Content Analysis
// ============================================

// Sessions with actual text content (preview first 100 chars)
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.text IS NOT NULL AND c.text <> ""
RETURN s.sessiontype, s.sessionguid, substring(c.text, 0, 100) as ContentPreview
LIMIT 10;

// Content types distribution
MATCH (c:Content)
WHERE c.contentType IS NOT NULL
RETURN c.contentType as ContentType, count(*) as Count
ORDER BY Count DESC;

// Sessions with multiple content items
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WITH s, count(c) as ContentCount
WHERE ContentCount > 1
RETURN s.sessionguid, s.sessiontype, ContentCount
ORDER BY ContentCount DESC
LIMIT 10;

// ============================================
// SECTION 4: Device and Account Relationships
// ============================================

// Devices with their associated phones and owners
MATCH (d:Device)-[:HAS_ACCOUNT]->(ph:Phone)
OPTIONAL MATCH (p:Person)-[:USES_DEVICE]->(d)
RETURN p.name as Person, d.imei as Device, collect(DISTINCT ph.number) as PhoneNumbers;

// People with multiple communication methods
MATCH (p:Person)-[:USES]->(comm)
WITH p, collect(labels(comm)[0] + ': ' + COALESCE(comm.number, comm.email, 'N/A')) as Methods
WHERE size(Methods) > 1
RETURN p.name as Person, Methods
ORDER BY size(Methods) DESC;

// ============================================
// SECTION 5: Network Analysis
// ============================================

// Communication pairs (who talks to whom)
MATCH (p1:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(p2:Person)
WHERE p1.name < p2.name  // Avoid duplicates
WITH p1.name as Person1, p2.name as Person2, count(DISTINCT s) as SharedSessions
ORDER BY SharedSessions DESC
LIMIT 15
RETURN Person1, Person2, SharedSessions;

// Most connected people (by unique contacts)
MATCH (p:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(other:Person)
WHERE p <> other
WITH p, count(DISTINCT other) as UniqueContacts
ORDER BY UniqueContacts DESC
LIMIT 10
RETURN p.name as Person, UniqueContacts;

// ============================================
// SECTION 6: Time-based Analysis
// ============================================

// Sessions by hour of day
MATCH (s:Session)
WHERE s.createddate IS NOT NULL
RETURN s.createddate.hour as Hour, count(*) as SessionCount
ORDER BY Hour;

// Recent sessions (last 7 days from latest session)
MATCH (s:Session)
WHERE s.createddate IS NOT NULL
WITH max(s.createddate) as LatestDate
MATCH (s2:Session)
WHERE s2.createddate >= LatestDate - duration({days: 7})
RETURN s2.sessionguid, s2.sessiontype, s2.createddate
ORDER BY s2.createddate DESC
LIMIT 20;

// ============================================
// SECTION 7: Visualization Queries
// ============================================

// Network around a specific person (2 degrees)
// Change the name to explore different people
MATCH path = (p:Person {name: '@Eagle, William'})-[*1..2]-(connected)
RETURN path
LIMIT 50;

// Session participation graph (small sample)
MATCH (s:Session)<-[:PARTICIPATED_IN]-(participant)
WITH s, collect(participant) as participants
WHERE size(participants) >= 2
WITH s, participants LIMIT 5
UNWIND participants as p
MATCH (p)-[:PARTICIPATED_IN]->(s)
RETURN p, s;

// ============================================
// SECTION 8: Data Quality Checks
// ============================================

// Sessions without content
MATCH (s:Session)
WHERE NOT (s)-[:HAS_CONTENT]->()
RETURN count(s) as SessionsWithoutContent;

// People without any communication method
MATCH (p:Person)
WHERE NOT (p)-[:USES]->()
RETURN p.name as PersonWithoutComms;

// Orphaned phones (not used by anyone)
MATCH (ph:Phone)
WHERE NOT ()<-[:USES]-(ph)
RETURN ph.number as OrphanedPhone;