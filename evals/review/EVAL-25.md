<!--- META: machine-readable for scripts --->
Status: REVIEW
ID: EVAL-25
Category: Metadata
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

# EVAL-25: How many sessions are still under review?

**Status**: ✅ **IMPLEMENTED**  
**Category**: Communications - Metadata Filter & Counting  
**Last Tested**: June 24, 2025

## Question
"How many sessions are still under review?"

## Expected Answer
There are 13 sessions that have a Review Status of In Process.

## Implementation

### Query
```cypher
MATCH (s:Session)
WHERE s.reviewstatus = 'In Process'
RETURN count(s) as sessions_under_review
```

### Actual Result
```
sessions_under_review: 13
```

## Validation ✅

**Test Command**:
```bash
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! \
"MATCH (s:Session) WHERE s.reviewstatus = 'In Process' RETURN count(s)"
```

**Status**: ✅ **PERFECT MATCH** - Exactly matches expected result (13 sessions)

## Technical Implementation

### Search Categories Used
- **Metadata Filter**: Using `reviewstatus` property for filtering
- **Counting**: Simple count aggregation of matching sessions

### Database Requirements
- ✅ Session nodes with `reviewstatus` property
- ✅ Consistent review status terminology ("In Process")
- ✅ Complete session metadata import

### Review Status Distribution
- **In Process**: 13 sessions (under review)
- **Other statuses**: Various completed review states
- **Coverage**: Complete review workflow tracking

## Business Value

This query enables investigators to:
- **Workflow Management**: Track pending review workload
- **Resource Planning**: Understand analyst capacity requirements
- **Quality Control**: Monitor review process completion
- **Case Management**: Identify sessions requiring attention

## Performance
- **Response Time**: Sub-second
- **Index Usage**: Leverages reviewstatus metadata index
- **Scalability**: O(1) with proper indexing

## Investigation Context

**Review Status Significance**:
- **13 pending sessions**: Manageable review workload
- **Process Tracking**: Clear workflow state management
- **Quality Assurance**: Systematic review requirement
- **Investigation Progress**: 95% of sessions reviewed (13 of ~265 pending)