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

## Test Query

```cypher
// Search for sago palm references across all content
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago palms') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(phone:Phone)-[:USED_BY]->(p:Person)
RETURN 
    s.sessionGuid,
    p.displayName,
    s.startTime,
    substring(node.text, 0, 200) as excerpt,
    score
ORDER BY score DESC
LIMIT 10;
```

## Expected Results

```
Found multiple sago palm references:
- William → Eagles Landscaping: Orders 2 sago palms from Florida nursery
- William → Ted: "Freddy will pick up the palms when down south" 
- William → Eagles Landscaping: "Fred will be late (7pm)" for palm pickup
```

## Business Value

- **Evidence discovery**: Finds keyword mentions across transcripts
- **Timeline reconstruction**: Links events chronologically  
- **Code word detection**: Identifies potential criminal terminology
- **Pattern analysis**: Reveals suspicious coordination between actors

## Confidence Assessment

**Fixed Query** (corrected relationship pattern):
```cypher
MATCH (s)<-[:PARTICIPATED_IN]-(phone:Phone)<-[:USES]-(p:Person)
```

**Query Results**: 10 sago palm references found with scores 4.2-5.5
**Key Findings**: 
- ✅ Eagles Landscaping ordering "two Sago Palms"
- ✅ William Eagle coordinating pickup 
- ✅ Multiple conversations about sago palms from Florida nursery

✅ **Correct** = Query successfully finds all expected sago palm references after relationship fix

**Confidence**: 90% → Auto-promote to PASSED

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