<!--- META: machine-readable for scripts --->
Status: PASSED
ID: EVAL-08
Category: Search
Added: 2025-07-03
Last-Run: 2025-07-03T09:27:27.823381
Duration-ms: —
Run-Count: 1
Blocker: —

# EVAL-08: Are there any references to sago palms?

**Status**: ✅ **IMPLEMENTED**  
**Implementation Date**: June 23, 2025  
**Feature**: Lucene full-text search on call transcripts and content

### Query

```cypher
// Search for sago palm references across all content
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago palms') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(phone:Phone)<-[:USES]-(p:Person)
RETURN 
    s.sessionguid,
    p.name,
    s.starttime,
    substring(node.text, 0, 200) as excerpt,
    score
ORDER BY score DESC
LIMIT 10;
```

## Expected Results

**Query Returns**: 10 results with scores 2.89-6.08

**Top Results**:
- Eagles Maintenance ordering "two Sago Palms to be picked up later" (score: 6.08)
- William Eagle: "told Kerry to order a couple of Sago Palms from that other place" (score: 5.53)  
- William Eagle: "arrangements to buy a couple of Sago palms" (score: 4.87)
- William Eagle: "increase that Sago Palm order from two to six" (score: 2.99)

**Key Pattern**: Sago palms are consistently discussed in context of landscaping business and shipments from South Florida.

## Business Value

- **Evidence discovery**: Finds keyword mentions across transcripts
- **Timeline reconstruction**: Links events chronologically  
- **Code word detection**: Identifies potential criminal terminology
- **Pattern analysis**: Reveals suspicious coordination between actors

## Confidence Assessment

**Schema Issues Fixed**:
- ❌ `s.sessionGuid` → ✅ `s.sessionguid` (property name case)
- ❌ `p.displayName` → ✅ `p.name` (correct property name)  
- ❌ `s.startTime` → ✅ `s.starttime` (property name case)
- ❌ `[:USED_BY]` → ✅ `[:USES]` (correct relationship type)
- ❌ `-[:USES]->` → ✅ `<-[:USES]-` (correct direction)

**Actual Results**: 10 sago palm references found with scores 2.89-6.08
**Key Validation**: 
- ✅ Eagles Maintenance ordering "two Sago Palms to be picked up later"
- ✅ William Eagle coordinating sago palm orders with Kerry
- ✅ Discussion of increasing order "from two to six" sago palms
- ✅ South Florida nursery as consistent source

✅ **VALIDATED** = Query returns expected sago palm references with proper scoring

**Confidence**: 95% - Schema corrected, query validated with live data

## Technical Implementation

- **Full-text index**: `ContentFullText` on `Content.text`
- **Lucene scoring**: BM25 ranking for relevance
- **Multi-content types**: Searches calls, SMS, emails simultaneously
- **Context preservation**: Links back to sessions and participants

## Alternative Queries

```cypher
// Fuzzy search for variations
CALL db.index.fulltext.queryNodes('ContentFullText', 'sag*') 
YIELD node, score
RETURN substring(node.text, 0, 100), score
ORDER BY score DESC;

// Phrase search with proximity
CALL db.index.fulltext.queryNodes('ContentFullText', '"sago palms" OR "palm trees"')
YIELD node, score
RETURN node.text, score;
```

## Validation Command

```bash
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! << 'EOF'
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago palms') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN count(*) as total_mentions, 
       avg(score) as avg_relevance_score;
EOF
```

## Related Evaluations

- **EVAL-09**: "sago palms" → Same query pattern
- **EVAL-10**: "is anyone talking about sagos?" → Fuzzy matching
- **EVAL-14**: "summarize all conversations about cherry blasters" → Content summarization