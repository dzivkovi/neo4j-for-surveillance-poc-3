<!--- META: machine-readable for scripts --->
Status: PASSED
ID: EVAL-21
Category: Search
Added: 2025-07-03
Last-Run: 2025-07-07T18:40:59.777496+00:00
Duration-ms: 1μs
Blocker: —

# EVAL-21: Communications

## Question
What kinds of sessions are in the morning?

## Expected Answer
There are messaging, telephony, and email sessions in the morning (between 8am and 10am).

## Implementation

### Query
```cypher
// Find all session types during morning hours (8am-10am = 13-14 UTC) across all years
MATCH (s:Session)
WHERE s.starttime IS NOT NULL 
  AND s.starttime.hour >= 13 
  AND s.starttime.hour < 15
RETURN DISTINCT s.sessiontype AS session_type, count(s) AS count
ORDER BY session_type
```

### Actual Result
```
session_type: "Email", count: 2
session_type: "Messaging", count: 31  
session_type: "Telephony", count: 12

There are email, messaging, and telephony sessions in the morning (between 8am and 10am).
Total morning sessions: 45 (Email: 2, Messaging: 31, Telephony: 12)
```

## Validation
**Status**: ✅ **PASSED**

## Confidence Assessment

**Query Results**: Found all three session types mentioned in the expected answer during morning hours (8am-10am): Email (2 sessions), Messaging (31 sessions), and Telephony (12 sessions). This exactly matches the expected answer.

**Business Question**: "What kinds of sessions are in the morning?"

**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED

## Technical Implementation

### Search Categories Used
- **Time Filter**: Filtered sessions by starttime hour range (13-14 UTC = 8am-10am)
- **Metadata Search**: Retrieved sessiontype field to categorize session types
- **Summarization**: Grouped and counted sessions by type to provide comprehensive overview

## Business Value

This evaluation tests the system's ability to handle communications scenarios for law enforcement investigations.
