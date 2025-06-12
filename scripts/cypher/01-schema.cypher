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
CREATE VECTOR INDEX ContentVectorIndex IF NOT EXISTS
FOR (c:Content) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 384,
    `vector.similarity_function`: "COSINE"
  }
};
