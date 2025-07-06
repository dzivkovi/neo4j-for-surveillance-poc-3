// ========================================
// Neo4j Surveillance Analytics Schema
// Complete schema creation with constraints, indexes, and diagnostics
// ========================================
//
// This script creates ALL constraints and indexes needed for the surveillance
// analytics POC. It includes diagnostics to ensure everything is created properly.
//
// Usage: docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/01-create-schema.cypher

// ========================================
// PART 1: Show initial state
// ========================================
RETURN "=== INITIAL STATE ===" as message;
CALL db.labels() YIELD label RETURN "Labels: " + label as info;
SHOW CONSTRAINTS;
SHOW INDEXES;

// ========================================
// PART 2: Create uniqueness constraints
// ========================================
RETURN "=== CREATING CONSTRAINTS ===" as message;

// Session uniqueness - core entity
CREATE CONSTRAINT session_guid IF NOT EXISTS
FOR (s:Session) REQUIRE s.sessionguid IS UNIQUE;

// Communication endpoint uniqueness
CREATE CONSTRAINT phone_number IF NOT EXISTS
FOR (p:Phone) REQUIRE p.number IS UNIQUE;

CREATE CONSTRAINT email_addr IF NOT EXISTS
FOR (e:Email) REQUIRE e.email IS UNIQUE;

CREATE CONSTRAINT device_imei IF NOT EXISTS
FOR (d:Device) REQUIRE d.imei IS UNIQUE;

// Alias uniqueness for entity resolution
CREATE CONSTRAINT alias_raw_unique IF NOT EXISTS
FOR (a:Alias) REQUIRE a.rawValue IS UNIQUE;

// ========================================
// PART 3: Create range indexes for queries
// ========================================
RETURN "=== CREATING RANGE INDEXES ===" as message;

// Person name index (for entity queries)
CREATE INDEX person_name_index IF NOT EXISTS
FOR (p:Person) ON (p.name);

// Session temporal indexes
CREATE INDEX session_createddate IF NOT EXISTS
FOR (s:Session) ON (s.createddate);

CREATE INDEX session_sessiontype IF NOT EXISTS
FOR (s:Session) ON (s.sessiontype);

CREATE RANGE INDEX sessionDuration IF NOT EXISTS
FOR (s:Session) ON (s.durationinseconds);

// ========================================
// PART 4: Create full-text indexes
// ========================================
RETURN "=== CREATING FULL-TEXT INDEXES ===" as message;

// Content search index
CREATE FULLTEXT INDEX ContentFullText IF NOT EXISTS
FOR (c:Content) ON EACH [c.text];

// Alias search index
CREATE FULLTEXT INDEX AliasText IF NOT EXISTS
FOR (a:Alias) ON EACH [a.rawValue];

// ========================================
// PART 5: Create spatial index
// ========================================
RETURN "=== CREATING SPATIAL INDEX ===" as message;

// Drop any incorrect location index first
DROP INDEX location_coord IF EXISTS;

// Create correct POINT index for geospatial queries
CREATE POINT INDEX locationGeo IF NOT EXISTS
FOR (l:Location) ON (l.geo);

// ========================================
// PART 6: Create vector index for embeddings
// ========================================
RETURN "=== CREATING VECTOR INDEX ===" as message;

// Vector index for semantic similarity (1536 dimensions for OpenAI)
CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS
FOR (c:Content) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: "COSINE"
  }
};

// ========================================
// PART 7: Final verification
// ========================================
RETURN "=== FINAL VERIFICATION ===" as message;

RETURN "Constraints created:" as message;
SHOW CONSTRAINTS;

RETURN "Indexes created:" as message;
SHOW INDEXES;

RETURN "=== SCHEMA CREATION COMPLETE ===" as message;