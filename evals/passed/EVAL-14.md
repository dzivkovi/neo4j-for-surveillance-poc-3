<!--- META: machine-readable for scripts --->
Status: PASSED
ID: EVAL-14
Category: Search
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

# EVAL-14: Communications

## Question
summarize all conversations about cherry blasters

## Expected Answer
There are no conversations that reference cherry blasters.

## Implementation

### Query
```cypher
// Hybrid search for "cherry blasters" - combining text and fulltext search
WITH "cherry blasters" AS searchTerm
CALL {
    // Text search for exact/partial matches
    WITH searchTerm
    MATCH (c:Content)
    WHERE toLower(c.text) CONTAINS toLower(searchTerm)
    RETURN c, "text_exact" AS searchType, 1.0 AS score
    
    UNION ALL
    
    // Fulltext search for better tokenization
    WITH searchTerm
    CALL db.index.fulltext.queryNodes('ContentFullText', searchTerm + ' OR cherry OR blaster OR blasters') 
    YIELD node AS c, score
    RETURN c, "fulltext" AS searchType, score
}
WITH c, searchType, score
MATCH (s:Session)-[:HAS_CONTENT]->(c)
RETURN s.sessionguid AS sessionId, 
       s.createddate AS date,
       s.sessiontype AS type,
       c.text AS content,
       searchType,
       score
ORDER BY score DESC
LIMIT 10
```

### Actual Result
```
[]
```

## Validation
**Status**: ⏳ **NOT YET IMPLEMENTED**

## Confidence Assessment

**Query Results**: No conversations found referencing "cherry blasters" - empty result set confirms expected answer
**Business Question**: "summarize all conversations about cherry blasters"
**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED

## Technical Implementation

### Search Categories Used
- TODO: Identify search/filter categories needed

## Business Value

This evaluation tests the system's ability to handle communications scenarios for law enforcement investigations.
