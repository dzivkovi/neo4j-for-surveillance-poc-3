// ========================================
// Neo4j Surveillance Analytics Schema (Simple Version)
// Complete schema creation without diagnostics for reliable execution
// ========================================

// Create uniqueness constraints
CREATE CONSTRAINT session_guid IF NOT EXISTS
FOR (s:Session) REQUIRE s.sessionguid IS UNIQUE;

CREATE CONSTRAINT phone_number IF NOT EXISTS
FOR (p:Phone) REQUIRE p.number IS UNIQUE;

CREATE CONSTRAINT email_addr IF NOT EXISTS
FOR (e:Email) REQUIRE e.email IS UNIQUE;

CREATE CONSTRAINT device_imei IF NOT EXISTS
FOR (d:Device) REQUIRE d.imei IS UNIQUE;

CREATE CONSTRAINT alias_raw_unique IF NOT EXISTS
FOR (a:Alias) REQUIRE a.rawValue IS UNIQUE;

// Create range indexes
CREATE INDEX person_name_index IF NOT EXISTS
FOR (p:Person) ON (p.name);

CREATE INDEX session_createddate IF NOT EXISTS
FOR (s:Session) ON (s.createddate);

CREATE INDEX session_sessiontype IF NOT EXISTS
FOR (s:Session) ON (s.sessiontype);

CREATE RANGE INDEX sessionDuration IF NOT EXISTS
FOR (s:Session) ON (s.durationinseconds);

// Create full-text indexes
CREATE FULLTEXT INDEX ContentFullText IF NOT EXISTS
FOR (c:Content) ON EACH [c.text];

CREATE FULLTEXT INDEX AliasText IF NOT EXISTS
FOR (a:Alias) ON EACH [a.rawValue];

// Create spatial index
DROP INDEX location_coord IF EXISTS;
CREATE POINT INDEX locationGeo IF NOT EXISTS
FOR (l:Location) ON (l.geo);

// Create vector index
CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS
FOR (c:Content) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: "COSINE"
  }
};