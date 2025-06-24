# EVAL-69: What phone numbers is William using?

**Status**: ✅ **IMPLEMENTED**  
**Category**: Communications - Device Analysis & Entity Identification  
**Last Tested**: June 24, 2025

## Question
"What phone numbers is William using?"

## Expected Answer
Eagle, William is using the following phone numbers:
- 9366351931 (74 sessions)
- 9364254000 (5 sessions)

## Implementation

### Query
```cypher
MATCH (william:Person {name: '@Eagle, William'})-[:USES]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN phone.number as phone_number,
       count(DISTINCT s) as sessions_using_phone
ORDER BY sessions_using_phone DESC
```

### Actual Result
```
phone_number: "9366351931", sessions_using_phone: 74
phone_number: "9364254000", sessions_using_phone: 5
```

## Validation ✅

**Test Command**:
```bash
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! \
"MATCH (william:Person {name: '@Eagle, William'})-[:USES]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session) RETURN phone.number, count(DISTINCT s) ORDER BY count(DISTINCT s) DESC"
```

**Status**: ✅ **PERFECT MATCH** - Exactly matches expected results (74 and 5 sessions)

## Technical Implementation

### Search Categories Used
- **Entity Device Mapping**: Person-to-phone relationship analysis
- **Usage Frequency Analysis**: Session count aggregation per device
- **Device Identification**: Phone number enumeration for specific person

### Database Requirements
- ✅ Person nodes with accurate entity names
- ✅ Phone nodes with phone number properties
- ✅ USES relationships between persons and phones
- ✅ PARTICIPATED_IN relationships between phones and sessions

### Device Usage Pattern Analysis
- **Primary Phone**: 9366351931 (93.7% usage - 74/79 sessions)
- **Secondary Phone**: 9364254000 (6.3% usage - 5/79 sessions)
- **Total Sessions**: 79 communications across both devices
- **Usage Pattern**: Heavily concentrated on single primary device

## Business Value

This query enables investigators to:
- **Device Correlation**: Link specific phone numbers to individuals
- **Usage Pattern Analysis**: Understand device preferences and operational patterns
- **Evidence Targeting**: Focus surveillance efforts on primary communication devices
- **Network Mapping**: Identify all communication endpoints for key suspects

## Performance
- **Response Time**: Sub-second
- **Index Usage**: Leverages person, phone, and session relationship indexes
- **Scalability**: Efficient person-to-device traversal queries

## Investigation Context

**William's Phone Usage Profile**:
- **Device Strategy**: Primary phone (9366351931) for majority of communications
- **Secondary Device**: Limited use of backup/alternate phone (9364254000)
- **Operational Pattern**: 15:1 usage ratio suggests primary device preference
- **Investigation Focus**: Primary surveillance target should be 9366351931