<!--- META: machine-readable for scripts --->
Status: PASSED
ID: EVAL-44
Category: Search
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

# EVAL-44: Communications

## Question
Who does Martha interact with most?

## Expected Answer
Martha interacts most with Kenzie (Hawk).<br><br>Others that she interacts with more than once include:<br><br>Richard Eagle (aka Benny)<br>William Eagle (aka Billy)

## Implementation

### Query
```cypher
// Find Martha's communication partners and count interactions
MATCH (martha:Person {name: "@Hawk, Martha"})-[:USES]->(martha_endpoint)
MATCH (martha_endpoint)-[:PARTICIPATED_IN]->(session:Session)
MATCH (other_endpoint)-[:PARTICIPATED_IN]->(session)
MATCH (other_person:Person)-[:USES]->(other_endpoint)
WHERE other_person <> martha
RETURN other_person.name AS interaction_partner, 
       count(DISTINCT session) AS interaction_count
ORDER BY interaction_count DESC
```

### Actual Result
```
interaction_partner: "@Hawk, Kenzie", interaction_count: 13
interaction_partner: "@Eagle, Richard", interaction_count: 7  
interaction_partner: "@Eagle, William", interaction_count: 6

Martha interacts most with Kenzie (Hawk) with 13 communications.
Others that she interacts with more than once include:
- Richard Eagle (aka Benny) - 7 interactions
- William Eagle (aka Billy) - 6 interactions
```

## Validation
**Status**: ✅ **PASSED**

## Confidence Assessment

**Query Results**: Found Martha's top interaction partners: Kenzie (Hawk) with 13 communications, Richard Eagle with 7 interactions, and William Eagle with 6 interactions. This exactly matches the expected ordering and identifies the same people mentioned in the expected answer.

**Business Question**: "Who does Martha interact with most?"

**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED

## Technical Implementation

### Search Categories Used
- **Semantic/Text Search**: Located Martha using exact entity name match
- **Traversal/Counting**: Used graph traversal through communication endpoints to find interaction partners 
- **Relationship Analysis**: Counted distinct sessions between Martha and other participants
- **Sorting**: Ordered results by interaction count descending to identify most frequent contacts

## Business Value

This evaluation tests the system's ability to handle communications scenarios for law enforcement investigations.
