<!--- META: machine-readable for scripts --->
Status: PASSED
ID: EVAL-30
Category: Search
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

# EVAL-30: Communications

## Question
What languages are used within this case?

## Expected Answer
The following languages are used: English (200 items) and Spanish (1 item)

## Implementation

### Query
```cypher
MATCH (s:Session)
WHERE s.primarylanguage IS NOT NULL
RETURN s.primarylanguage as language, count(*) as session_count
ORDER BY session_count DESC
```

### Actual Result
```
Languages used in this case:

English: 200 items
Spanish: 1 item

Total sessions with language detection: 201
Sessions without language data: 64
```

## Validation
**Status**: ✅ **IMPLEMENTED**

## Confidence Assessment

**Query Results**: Identified English (200 items) and Spanish (1 item) languages in communications data
**Business Question**: "What languages are used within this case?"
**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED

## Technical Implementation

### Search Categories Used
- **Language Detection Analysis**: Uses primarylanguage property from automated language detection
- **Aggregation Queries**: Groups sessions by language with counts
- **Data Quality Assessment**: Identifies sessions with and without language metadata

## Business Value

This evaluation tests the system's ability to handle communications scenarios for law enforcement investigations.
