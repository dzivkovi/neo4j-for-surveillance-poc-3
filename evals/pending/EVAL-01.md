# EVAL-01: Does fred discuss travel plans?

**Status**: 🔄 **PARTIALLY WORKING**  
**Blocker**: Needs semantic search for "travel plans" concept  
**Current Capability**: Can find "Fred" mentions via Lucene

## Current Query (Partial)

```cypher
// This finds Fred mentions but misses semantic "travel" concepts
CALL db.index.fulltext.queryNodes('AliasText', 'Fred OR Freddy') 
YIELD node
MATCH (node)-[:ALIAS_OF]->(p:Person)
MATCH (p)<-[:USED_BY]-(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
MATCH (s)-[:HAS_CONTENT]->(c:Content)
WHERE c.text CONTAINS 'travel' OR c.text CONTAINS 'trip' OR c.text CONTAINS 'go'
RETURN s.sessionGuid, c.text
LIMIT 5;
```

## Expected Results (When Implemented)

```
Fred discusses travel plans in multiple instances:
- Feb 9, 2020: Tells Benny he's leaving next day
- Feb 11, 2020: Tells William finishing in Mobile, heading to Miami  
- Feb 12, 2020: Tells William "gassed up and ready to go"
- Feb 14, 2020: Tells William will be back next afternoon
```

## Implementation Requirements

### Missing Components
1. **Semantic search**: Vector embeddings to understand "travel plans" ≈ "leaving", "going", "trip", "journey"
2. **Context window**: Analyze conversation context, not just isolated phrases
3. **Entity resolution**: Merge "@Merlin, Fred" and "Freddy" aliases

### Technical Solution
```cypher
// Future implementation with vector search
CALL db.index.vector.queryNodes('content_embeddings', 'travel plans', 5)
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(phone:Phone)-[:USED_BY]->(p:Person)
WHERE p.displayName CONTAINS 'Fred'
RETURN s.sessionGuid, node.text, score;
```

## Business Value (When Complete)

- **Intent detection**: Understanding plans vs casual mentions
- **Timeline analysis**: Connecting travel plans to actual movements
- **Network mapping**: Who knows about Fred's travel plans?
- **Evidence correlation**: Linking discussions to physical evidence

## Blocking Dependencies

1. **Vector index creation**: Need embeddings for Content nodes
2. **Synonym expansion**: "travel", "trip", "journey", "go", "leave"
3. **Context analysis**: Conversation threading and summarization

## Estimated Implementation Effort

- **Vector embeddings**: 2-3 hours
- **Semantic query patterns**: 1-2 hours  
- **Testing and validation**: 1 hour
- **Total**: 4-6 hours

## Related Evaluations

- **EVAL-02**: French translation of same question
- **EVAL-03**: Uses "@Merlin, Fred" entity notation
- **EVAL-04**: "do freddy talk about traveling?" → Alias variations