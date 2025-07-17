# Data Mapping and Naming Convention Guide

This guide documents how data flows from source files into Neo4j, clarifying naming conventions to prevent confusion.

## Data Flow Overview

```
Source Files → Python Scripts → Neo4j Database
```

## 1. Source Data Formats

### sessions.ndjson (Primary Source)
```json
{
  "sessionguid": "339cb9df-232b-eba2-be7e-010a9216a298",
  "starttime": "2000-04-03T18:26:55.000000000Z",
  "stoptime": "2000-04-03T18:28:42.000Z",  
  "contenttype": "text/html",
  "reviewstatus": "Not Viewed",
  "durationinseconds": 107
}
```
- **Convention**: All lowercase, no underscores
- **Key field**: `sessionguid` (not session_guid or sessionGuid)
- **Time fields**: Source has `stoptime` (not `endtime`)

### transcripts.json (LanceDB Export)
```json
{
  "00fdfea0-8c72-487a-b726-513f6fafb338": {
    "text": "Hey, where are you?",
    "session_type": "Telephony",
    "content_type": "audio/x-wav",
    "timestamp": 1581376213
  }
}
```
- **Convention**: Python snake_case (underscores)
- **Key**: Session GUID value (not a field name)
- **Mapping**: `session_type` → Neo4j `sessionType`

## 2. Python Import Scripts

### Variable Naming vs Database Properties
```python
# Python variables use snake_case
session_id = rec["sessionguid"]  # Variable name doesn't match property

# But Cypher queries use correct Neo4j property names
tx.run("""
    MATCH (s:Session {sessionguid: $sid})
    SET s.contenttype = $ctype
""", sid=session_id, ctype=content_type)
```

### Key Principle
- **Internal Python**: `snake_case` variables
- **Neo4j Properties**: Lowercase, no underscores
- **Cypher Parameters**: Can be anything (they're just placeholders)

## 3. Neo4j Database Schema

### Session Node Properties
| Property | Type | Example | Source Field |
|----------|------|---------|--------------|
| sessionguid | STRING | "339cb9df-232b-eba2-be7e-010a9216a298" | sessionguid |
| starttime | DATETIME | 2000-04-03T18:26:55Z | starttime |
| stoptime | STRING | "2000-04-03T18:28:42.000Z" | stoptime |
| contenttype | STRING | "text/html" | contenttype |
| durationinseconds | INTEGER | 145 | durationinseconds or computed |
| sessiondate | DATE | 2000-04-03 | computed from starttime |

### Content Node Properties  
| Property | Type | Note |
|----------|------|------|
| contentType | STRING | ⚠️ CamelCase exception |
| text | STRING | Transcript or message text |
| embedding | LIST[FLOAT] | 1536-dimension vector |

## 4. Index Naming

### Current Indexes
```cypher
// Index names can differ from property names
CREATE INDEX session_guid FOR (s:Session) ON (s.sessionguid)
//            ^^^^^^^^^^^^                      ^^^^^^^^^^^
//            Index name                        Property name
```

### Index List
| Index Name | Property | Purpose |
|------------|----------|---------|
| session_guid | sessionguid | Unique session lookup |
| session_createddate | createddate | Temporal queries |
| sessionDuration | durationinseconds | Duration analysis |

## 5. Common Pitfalls and Solutions

### ❌ DON'T
- Assume Python variable names match Neo4j properties
- Use CamelCase for new properties (except Content.contentType)
- Mix naming conventions in Cypher queries

### ✅ DO  
- Check actual property names: `MATCH (s:Session) RETURN keys(s) LIMIT 1`
- Use lowercase for all new Neo4j properties
- Keep Python variables in snake_case internally

## 6. Quick Reference

### Data Transformation Pipeline
```
Source JSON          Python Variable    Neo4j Property      Notes
-----------          ---------------    --------------      -----
sessionguid      →   session_id     →   sessionguid
starttime        →   start_time     →   starttime  
stoptime         →   stop_time      →   stoptime           Direct import
contenttype      →   content_type   →   contenttype
durationinseconds →  duration       →   durationinseconds   Or computed
session_type     →   session_type   →   sessionType        Content node
-                →   -              →   sessiondate        Computed field
```

## 7. Validation Commands

### Check Property Names
```bash
# See actual Session properties
echo "MATCH (s:Session) RETURN keys(s)[0..10] LIMIT 1;" | \
  docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3!

# See actual Content properties  
echo "MATCH (c:Content) RETURN keys(c)[0..10] LIMIT 1;" | \
  docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3!
```

### Check Indexes
```bash
echo "SHOW INDEXES YIELD name, properties;" | \
  docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3!
```

## Summary

The key to avoiding confusion is understanding that:
1. **Source data** uses various conventions (lowercase, snake_case)
2. **Python scripts** use snake_case internally
3. **Neo4j properties** are mostly lowercase without underscores
4. **Index names** are arbitrary and don't need to match property names

### Critical Field Handling
- **stoptime**: Direct import from source, no mapping needed
- **sessiondate**: Computed field from `starttime`, not in source
- **durationinseconds**: Usually from source, computed if both times exist

### Dataset Variations
- **Whiskey Jack (Demo)**: Has stoptime for most sessions
- **Gantry (Real)**: No stoptime, but has durationinseconds for telephony

When in doubt, always check the actual database schema rather than assuming based on variable names or index names.