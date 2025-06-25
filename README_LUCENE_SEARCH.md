# Neo4j Full-text Search Guide

**What it is**: Neo4j's full-text search uses Apache Lucene under the hood, but Neo4j documentation calls it "full-text indexes". This guide shows practical search syntax that works with our surveillance POC.

## Prerequisites

Create a full-text index first:
```cypher
CREATE FULLTEXT INDEX ContentFullText FOR (c:Content) ON EACH [c.text]
```

Check existing indexes:
```cypher
SHOW FULLTEXT INDEXES
```

## Basic Search Syntax

### 1. Simple Text Search
```cypher
// Find exact word
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago') YIELD node, score
RETURN node.text, score
```

### 2. Fuzzy Search (~)
```cypher
// Find variations with 1 character difference
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago~1') YIELD node, score
// Matches: "sago", "sagos", "sage"

// Allow 2 character differences
CALL db.index.fulltext.queryNodes('ContentFullText', 'travel~2') YIELD node, score
// Matches: "travel", "travels", "traveled"
```

### 3. Wildcard Search
```cypher
// * = any number of characters
CALL db.index.fulltext.queryNodes('ContentFullText', 'trav*') YIELD node, score
// Matches: "travel", "traveling", "travis", "traverse"

// ? = single character
CALL db.index.fulltext.queryNodes('ContentFullText', 'b?g') YIELD node, score
// Matches: "bag", "big", "bug"
```

### 4. Phrase Search
```cypher
// Exact phrase (use double quotes)
CALL db.index.fulltext.queryNodes('ContentFullText', '"South Florida"') YIELD node, score
// Only matches exact phrase "South Florida"
```

### 5. Boolean Operators
```cypher
// AND - both terms required
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago AND palm') YIELD node, score

// OR - either term
CALL db.index.fulltext.queryNodes('ContentFullText', 'travel OR trip') YIELD node, score

// NOT - exclude term
CALL db.index.fulltext.queryNodes('ContentFullText', 'travel NOT hotel') YIELD node, score

// Grouping with parentheses
CALL db.index.fulltext.queryNodes('ContentFullText', '(sago OR palm) AND Florida') YIELD node, score
```

### 6. Proximity Search
```cypher
// Find words within N positions of each other
CALL db.index.fulltext.queryNodes('ContentFullText', '"sago palm"~5') YIELD node, score
// Finds "sago" within 5 words of "palm"
```

### 7. Boosting Terms (^)
```cypher
// Make certain terms more important
CALL db.index.fulltext.queryNodes('ContentFullText', 'travel^2 OR vacation') YIELD node, score
// "travel" has 2x weight compared to "vacation"
```

### 8. Range Queries
```cypher
// Alphabetic/numeric ranges (if field supports it)
CALL db.index.fulltext.queryNodes('ContentFullText', '[A TO C]') YIELD node, score
```

### 9. Escaping Special Characters
```cypher
// Use backslash to escape: + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /
CALL db.index.fulltext.queryNodes('ContentFullText', 'what\\?') YIELD node, score
// Searches for literal "what?"
```

## Combining with Graph Queries

### Find Who Said What
```cypher
CALL db.index.fulltext.queryNodes('ContentFullText', 'sago~1') YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-()-[:USES]-(p:Person)
RETURN p.name as speaker, substring(node.text, 0, 200) as snippet, score
ORDER BY score DESC
```

### Search Multiple Terms with Context
```cypher
CALL db.index.fulltext.queryNodes('ContentFullText', 
  'travel* OR trip* OR vacation*') YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN s.sessionguid, datetime(s.starttime) as when, 
       substring(node.text, 0, 300) as snippet
ORDER BY when
```

## Common Patterns in This POC

### Search Communications Content
```cypher
// Our main index
ContentFullText - searches Content.text property

// Example queries that work:
'sago~1'           // Finds sago, sagos
'shed'             // Finds shed references  
'"rock salt"'      // Exact phrase
'track*'           // Finds tracking, track, tracked
```

### Search Person Names/Aliases
```cypher
// Alias index
AliasText - searches Alias.rawValue property

// Example queries:
'william~1'        // Finds William, Williams
'kenny~2'          // Might find Kenzie
```

## Tips for Effective Searches

1. **Start specific, then broaden**:
   - Try exact: `"sago palm"`
   - Then fuzzy: `sago~1`
   - Then wildcard: `sag*`

2. **Combine search types**:
   ```cypher
   '"exact phrase" OR fuzzy~1 OR wild*'
   ```

3. **Use score for relevance**:
   ```cypher
   ORDER BY score DESC
   ```

4. **Limit results for performance**:
   ```cypher
   LIMIT 20
   ```

## Available Indexes in This POC

Check what you can search:
```cypher
SHOW FULLTEXT INDEXES
```

Current indexes:
- `ContentFullText` - Communication content text
- `AliasText` - Name variations and aliases

## Troubleshooting

**"No such fulltext schema index"**
- Check index name spelling
- Verify index exists with `SHOW FULLTEXT INDEXES`

**No results**
- Try fuzzy search (~1 or ~2)
- Use wildcards (*)
- Check if content exists: `MATCH (c:Content) RETURN c.text LIMIT 5`

**Slow queries**
- Add LIMIT
- Use more specific terms
- Avoid leading wildcards (*term)

## References

- [Neo4j Full-text Search Docs](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/full-text-indexes/)
- [Lucene Query Syntax](https://lucene.apache.org/core/9_11_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#package.description)

Remember: Neo4j's full-text search is powered by Apache Lucene but configured through Cypher. The syntax above works with Neo4j 5.x.
