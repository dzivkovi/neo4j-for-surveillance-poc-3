// Comprehensive schema validation and fix script
// Ensures all indexes and constraints match the original neo4j-sessions setup
//
// Run with: docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/05-validate-and-fix-schema.cypher

// ========================================
// PART 1: Show current state
// ========================================
SHOW CONSTRAINTS;
SHOW INDEXES;

// ========================================
// PART 2: Ensure all constraints exist
// ========================================

// These constraints automatically create backing RANGE indexes
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

// ========================================
// PART 3: Create missing RANGE indexes
// ========================================

// Person name index (not covered by constraint)
CREATE INDEX person_name IF NOT EXISTS
FOR (p:Person) ON (p.name);

// Session indexes for common queries
CREATE INDEX session_createddate IF NOT EXISTS
FOR (s:Session) ON (s.createddate);

CREATE INDEX session_sessiontype IF NOT EXISTS
FOR (s:Session) ON (s.sessiontype);

CREATE RANGE INDEX sessionDuration IF NOT EXISTS
FOR (s:Session) ON (s.durationinseconds);

// ========================================
// PART 4: Full-text indexes
// ========================================

CREATE FULLTEXT INDEX ContentFullText IF NOT EXISTS
FOR (c:Content) ON EACH [c.text];

CREATE FULLTEXT INDEX AliasText IF NOT EXISTS
FOR (a:Alias) ON EACH [a.rawValue];

// ========================================
// PART 5: Spatial index
// ========================================

// First drop the wrong type if it exists
DROP INDEX location_coord IF EXISTS;

// Create the correct POINT index
CREATE POINT INDEX locationGeo IF NOT EXISTS
FOR (l:Location) ON (l.geo);

// ========================================
// PART 6: Vector index (already correct in scripts/01-create-schema.sh)
// ========================================

CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS
FOR (c:Content) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: "COSINE"
  }
};

// ========================================
// PART 7: Final validation
// ========================================

// Show final state
RETURN "=== FINAL CONSTRAINT COUNT ===" as message;
SHOW CONSTRAINTS;

RETURN "=== FINAL INDEX COUNT ===" as message;
SHOW INDEXES;