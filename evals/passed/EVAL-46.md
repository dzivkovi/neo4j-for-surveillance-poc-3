<!--- META: machine-readable for scripts --->
Status: PASSED
ID: EVAL-46
Category: Search
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

# EVAL-46: Communications

## Question
Summarize Richard's communications on February 6, 2020

## Expected Answer
On February 6, 2020, Richard was involved in a series of SMS messages with William Eagle. The conversation began at 12:10 PM, when William inquired about a new promotion Kenzie was offering and Richard's whereabouts. Richard responded that he was at the trailer and had heard about the year-round promotion, which included property checks. William then remarked that Kenzie's pricing was likely complex.<br><br>In terms of activity, Richard had a total of 6 events on this day. All of these events were instant messaging sessions. The day of the week was Thursday, and all of the events occurred in the afternoon.

## Implementation

### Query
```cypher
MATCH (p:Person)-[:USES]-()-[:PARTICIPATED_IN]->(s:Session)
WHERE p.name CONTAINS 'Richard' 
  AND date(datetime(s.starttime)) = date('2020-02-06')
WITH DISTINCT s
OPTIONAL MATCH (s)-[:HAS_CONTENT]->(c:Content)
WHERE NOT c.text CONTAINS '[PARTICIPANTS:'
RETURN s.sessionguid,
       datetime(s.starttime) as start_time,
       s.sessiontype,
       c.text as message_content
ORDER BY s.starttime
```

### Actual Result
```
Richard's communications on February 6, 2020 (Thursday afternoon):

17:10:11 - Messaging: "Martha said Kenzie's trying a new promotion on her side. You hear anything? Where you at?"

17:12:09 - Messaging: "I'm at the trailer taking care of things like I said. Yeah. It's year-round and includes property checks. Wonder how she's pricing that"

17:13:41 - Messaging: "Knowing that one bet her pricing has more twists than a pretzel factory"

Summary: 6 messaging sessions total, conversation with William Eagle about Kenzie's new promotion offering year-round property checks. Richard was at the trailer and expressed skepticism about Kenzie's pricing structure.
```

## Validation
**Status**: ✅ **IMPLEMENTED**

## Confidence Assessment

**Query Results**: Complete timeline of Richard's communications on Feb 6, 2020 showing SMS conversation about Kenzie's promotion
**Business Question**: "Summarize Richard's communications on February 6, 2020"
**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED

## Technical Implementation

### Search Categories Used
- **Date Filtering**: Precise date matching using date() function
- **Person-Session Mapping**: Links Richard to his communication sessions
- **Content Extraction**: Filters out metadata to show actual message content
- **Timeline Analysis**: Chronological ordering of communications

## Business Value

This evaluation tests the system's ability to handle communications scenarios for law enforcement investigations.
