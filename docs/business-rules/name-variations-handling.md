# Name Variations Handling

**Source**: Fred investigation analysis  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: High  
**Implementation**: [pending]  

## Problem
Same person appears with different name variations in the data, causing failed entity resolution in queries.

## Rule
Handle aliases like Fred/Freddy/@Merlin, Fred as referring to the same person.

**Options to evaluate:**
1. **Pre-mapping**: Create alias relationships during import
2. **Dynamic resolution**: Handle variations at query time using fuzzy matching

## Implementation Details

### Option 1: Pre-mapping (Recommended)
```cypher
// Create alias relationships
CREATE (fred:Person {name: '@Merlin, Fred'})
SET fred.aliases = ['Fred', 'Freddy', 'Merlin, Fred', '@Merlin, Fred']

// Or separate Alias nodes
CREATE (fred:Person {name: '@Merlin, Fred'})
CREATE (a1:Alias {name: 'Fred'})
CREATE (a2:Alias {name: 'Freddy'})
CREATE (fred)-[:ALSO_KNOWN_AS]->(a1)
CREATE (fred)-[:ALSO_KNOWN_AS]->(a2)
```

### Option 2: Dynamic Resolution
```cypher
MATCH (p:Person)
WHERE p.name =~ '(?i).*(fred|freddy|merlin).*'
RETURN p
```

## Related
- #eval-1, #eval-3, #eval-4 (Fred variations in queries)
- Entity resolution improvements

## Notes
DGraph handles this through their hybrid search with vector similarity. Need to decide if we want manual mapping or automated similarity matching.