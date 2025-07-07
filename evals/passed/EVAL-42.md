<!--- META: machine-readable for scripts --->
Status: PASSED
ID: EVAL-42
Category: Search
Added: 2025-07-03
Last-Run: 2025-07-07T18:40:59.777496+00:00
Duration-ms: 1μs
Blocker: —

# EVAL-42: Communications

## Question
when does <@Hawk, Kenzie> normally talk with William?

## Expected Answer
Kenzie and William have only communicated on Fridays and Saturdays. Specifically, these occurred only on February 7 2020 and February 15 2020.

## Implementation

### Query
```cypher
// Complete analysis: When does Kenzie normally talk with William?
MATCH (kenzie:Person {name: "@Hawk, Kenzie"})-[:USES]->(kenzie_endpoint)
MATCH (william:Person {name: "@Eagle, William"})-[:USES]->(william_endpoint)
MATCH (kenzie_endpoint)-[:PARTICIPATED_IN]->(session:Session)
MATCH (william_endpoint)-[:PARTICIPATED_IN]->(session)
WITH DISTINCT 
  date(session.starttime) AS communication_date,
  CASE session.starttime.dayOfWeek 
    WHEN 1 THEN "Monday"
    WHEN 2 THEN "Tuesday" 
    WHEN 3 THEN "Wednesday"
    WHEN 4 THEN "Thursday"
    WHEN 5 THEN "Friday"
    WHEN 6 THEN "Saturday"
    WHEN 7 THEN "Sunday"
  END AS day_of_week_name,
  count(session) AS session_count
RETURN communication_date, day_of_week_name, session_count
ORDER BY communication_date
```

### Actual Result
```
communication_date: "2020-02-07", day_of_week_name: "Friday", session_count: 4
communication_date: "2020-02-15", day_of_week_name: "Saturday", session_count: 8

Kenzie and William have only communicated on Fridays and Saturdays.
Specifically, these occurred only on February 7 2020 (Friday) and February 15 2020 (Saturday).
```

## Validation
**Status**: ✅ **PASSED**

## Confidence Assessment

**Query Results**: Found that Kenzie and William communicated on exactly two dates: February 7, 2020 (Friday) and February 15, 2020 (Saturday). This perfectly matches the expected answer stating they only communicated on Fridays and Saturdays on these specific dates.

**Business Question**: "when does <@Hawk, Kenzie> normally talk with William?"

**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED

## Technical Implementation

### Search Categories Used
- **Semantic/Text Search**: Located specific persons using exact entity name matches
- **Combination Search**: Found sessions where both Kenzie AND William participated  
- **Metadata Search**: Retrieved communication times and extracted dates/days of week
- **Summarization**: Analyzed temporal patterns to identify communication schedule

## Business Value

This evaluation tests the system's ability to handle communications scenarios for law enforcement investigations.
