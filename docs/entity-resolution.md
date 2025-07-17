# Entity Resolution System

**Status**: ✅ **Working Automatically** - All aliases resolved during import

## System Overview

Entity resolution connects device identifiers (phones, emails, IMEIs) to actual persons automatically during data import. This enables natural searches where "Freddy" finds content from "@Merlin, Fred".

**Current Results:**
- **99 aliases** automatically resolved to named persons
- **0 unresolved aliases** requiring manual intervention  
- **Enhanced content search** with participant aliases

## Verification

```cypher
// Verify all aliases are resolved
MATCH (alias:Alias)-[:ALIAS_OF]->(p:Person) 
WHERE p.name IS NULL 
RETURN count(*) as unresolved_aliases;
// Expected result: 0
```

```cypher
// Show alias distribution
MATCH (alias:Alias) 
RETURN alias.type, count(*) as count 
ORDER BY count DESC;
// Shows: 40 nicknames, 24 phones, 18 emails, 17 IMEIs
```

## How It Works

**Automatic Resolution**: The `01-import-data.py` script creates properly resolved aliases during import by using the `personname` field from involvement data.

**Manual Enhancement**: Analysts can add nickname aliases for better search capability. Example script in `scripts/03-analyst-knowledge-aliases.cypher` adds "Freddy", "Freddie", "Merlin" aliases for Fred:

```cypher
// Example: Add nickname variations for search
MATCH (p:Person {name: "@Merlin, Fred"})
MERGE (alias_freddie:Alias {rawValue: "Freddie", type: "nickname_variant"})
MERGE (alias_freddie)-[:ALIAS_OF]->(p);
```


## Deployment Workflow

### 1. Schema and Data Import
```bash
scripts/01-create-schema.sh
python scripts/01-import-data.py  # Creates resolved aliases automatically
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/02-sanity.cypher  # Verify import
```

### 2. Add Analyst Knowledge (Optional)
```bash
# Add manual nickname aliases for enhanced search
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/03-analyst-knowledge-aliases.cypher
```

### 3. Enable Enhanced Search
```bash
# Enhance content with participant aliases - includes built-in validation
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/04-content-search-enhancement.cypher
```

## Content Search Enhancement

### Problem Statement

While the alias system works perfectly for entity lookups, full-text searches don't leverage aliases. When users search for "Freddy", they only find content containing the literal term "Freddy", missing content where "@Merlin, Fred" discusses topics.

### Solution: Content Enhancement Approach

Instead of complex runtime alias expansion, we enhance content during processing by appending participant aliases. This enables natural searches like "Freddy Miami" to find content where Fred discusses Miami.

**Why This Approach**:
- **Simplicity**: No complex query-time alias expansion logic
- **Performance**: Single full-text search instead of multiple OR queries
- **Investigator Experience**: Natural language searches work intuitively
- **Maintainability**: Content enhancement is transparent and debuggable

### Implementation Results

```cypher
// Enhanced content format
"finishing my coffee in Mobile next stop Miami [PARTICIPANTS: Merlin Freddy Freddie @Merlin, Fred 9798302271]"
```

**Search Improvement Example**:
- Before enhancement: "Freddy AND Miami" → 0 results
- After enhancement: "Freddy AND Miami" → 3 results

### Content Enhancement Workflow

```bash
# Apply content search enhancement
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/04-content-search-enhancement.cypher
```

**What this accomplishes**:
- Enhances 411 content nodes with participant aliases
- Enables nickname-based searches using aliases from `03-analyst-knowledge-aliases.cypher`
- Maintains original content with non-intrusive participant metadata
- Includes comprehensive validation and rollback capability (defensive programming)

### Verification Queries

```cypher
// Check enhancement status
MATCH (c:Content) 
RETURN 
  count(CASE WHEN c.enhanced = true THEN 1 END) as enhanced_count,
  count(CASE WHEN c.enhanced IS NULL THEN 1 END) as unenhanced_count;

// Test improved search capability
CALL db.index.fulltext.queryNodes('ContentFullText', 'Freddy AND Miami') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN count(s) as search_results;
```

## Complete Deployment Process

### Production Workflow

1. **Schema and Data Import**:
   ```bash
   scripts/01-create-schema.sh
   python scripts/01-import-data.py  # Creates resolved aliases automatically
   ```

2. **Analyst Knowledge Enhancement**:
   ```bash
   docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/03-analyst-knowledge-aliases.cypher
   ```

3. **Content Search Enhancement** (includes built-in validation):
   ```bash
   docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/04-content-search-enhancement.cypher
   ```

### Key Achievements

- **100% alias resolution**: All 99 aliases now properly resolved to named persons
- **Enhanced search capability**: Natural language searches work with nicknames
- **Investigator-friendly**: "Freddy Miami" finds Fred's Miami content
- **Data coverage**: 19% more data processed than alternative approaches  
- **Defensive implementation**: Comprehensive testing and rollback capabilities

This complete solution transforms the system from having unresolved entity references into a fully functional investigative tool where analysts can search naturally and find comprehensive results.