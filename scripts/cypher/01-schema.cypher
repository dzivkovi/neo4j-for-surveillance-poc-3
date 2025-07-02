/**************************************************************************
  Session-Centric POLE Schema
**************************************************************************/

// —— Constraints (uniqueness) ———————————————
CREATE CONSTRAINT session_guid IF NOT EXISTS
FOR (s:Session) REQUIRE s.sessionguid IS UNIQUE;

CREATE CONSTRAINT phone_number IF NOT EXISTS
FOR (p:Phone) REQUIRE p.number IS UNIQUE;

CREATE CONSTRAINT email_addr IF NOT EXISTS
FOR (e:Email) REQUIRE e.email IS UNIQUE;

CREATE CONSTRAINT device_imei IF NOT EXISTS
FOR (d:Device) REQUIRE d.imei IS UNIQUE;

// —— Property indexes for fast lookup ———————————
CREATE INDEX session_createddate IF NOT EXISTS
FOR (s:Session) ON (s.createddate);

CREATE INDEX session_sessiontype IF NOT EXISTS
FOR (s:Session) ON (s.sessiontype);

CREATE INDEX person_name IF NOT EXISTS
FOR (p:Person) ON (p.name);

CREATE INDEX location_coord IF NOT EXISTS
FOR (l:Location) ON (l.coord);

// —— Full-Text index on unstructured content —————————
// CALL db.index.fulltext.createNodeIndex(
//   "ContentFullText", ["Content"], ["text"]
// );
CREATE FULLTEXT INDEX ContentFullText IF NOT EXISTS
FOR (c:Content) ON EACH [c.text];

// —— Vector index for semantic similarity ——————————
// Updated to 1536 dimensions for OpenAI embeddings (was 384 for sentence-transformers)
CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS
FOR (c:Content) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: "COSINE"
  }
};

// —— Feature #7: Transcripts & Lucene Search Additions ——————————

// Drop existing location index (wrong type)
DROP INDEX location_coord IF EXISTS;

// Point index for spatial queries
CREATE POINT INDEX locationGeo IF NOT EXISTS
FOR (l:Location) ON (l.geo);

// Range index for temporal/duration queries  
CREATE RANGE INDEX sessionDuration IF NOT EXISTS
FOR (s:Session) ON (s.durationinseconds);

// Full-text index for alias searches
CREATE FULLTEXT INDEX AliasText IF NOT EXISTS
FOR (a:Alias) ON EACH [a.rawValue];

// Uniqueness constraint for aliases
CREATE CONSTRAINT alias_raw_unique IF NOT EXISTS
FOR (a:Alias) REQUIRE a.rawValue IS UNIQUE;
