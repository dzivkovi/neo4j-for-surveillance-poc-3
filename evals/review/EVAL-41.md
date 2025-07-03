<!--- META: machine-readable for scripts --->
Status: REVIEW
ID: EVAL-41
Category: Search
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

# EVAL-41: How do Kenzie and William communicate?

**Status**: ✅ **IMPLEMENTED**  
**Category**: Communications - Entity Relationship Analysis  
**Last Tested**: June 24, 2025

## Question
"How doe Kenzie and William communicate?"

## Expected Answer
Kenzie and William have exclusively communicated through SMS/messaging. They have exchanged a total of 12 messages about family matters and business operations.

## Implementation

### Query
```cypher
MATCH (k:Person {name: '@Hawk, Kenzie'})-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(w:Person {name: '@Eagle, William'})
RETURN s.sessiontype as communication_method, 
       count(*) as session_count
ORDER BY session_count DESC
```

### Actual Result
```
communication_method: "Messaging", session_count: 12
```

## Validation ✅

**Status**: ✅ **PERFECT MATCH** - Exactly 12 messaging sessions, exclusively SMS/messaging as expected

## Technical Implementation

### Search Categories Used
- **Entity Relationship Analysis**: Specific person-to-person communication analysis
- **Communication Method Classification**: Session type identification
- **Exclusive Channel Analysis**: Single communication method verification

### Database Requirements
- ✅ Person nodes with accurate entity names
- ✅ USES and PARTICIPATED_IN relationship chains
- ✅ Session type metadata classification

## Business Value

This query enables investigators to:
- **Relationship Profiling**: Understand communication patterns between key suspects
- **Channel Analysis**: Identify preferred communication methods
- **Evidence Focus**: Concentrate on specific communication channels
- **Network Mapping**: Map communication relationships in suspect network

## Investigation Context

**Kenzie-William Communication Profile**:
- **Exclusive Method**: 100% messaging (no voice calls)
- **Communication Volume**: 12 total sessions
- **Relationship Type**: Business/family coordination
- **Investigation Focus**: Text-based evidence analysis priority