/*
Analyst Knowledge Enhancement - Manual Alias Creation
=====================================================

This script adds analyst-discovered aliases that automated entity resolution
cannot detect, such as:
- Nickname variations (Freddie -> Fred)
- Common name shortcuts (Bill -> William) 
- Analyst investigation findings
- Manual entity resolution corrections

Run AFTER: scripts/01-create-schema.sh, 02-import-sessions.py
Purpose: Enhance automated entity resolution with human intelligence
*/

-- ============================================================================
-- FREDDIE/FRED MERLIN ALIASES
-- ============================================================================

-- Create common nickname variations analysts would search for
MATCH (p:Person {name: "@Merlin, Fred"})
MERGE (alias_freddie:Alias {rawValue: "Freddie", type: "nickname_variant"})
MERGE (alias_freddie)-[:ALIAS_OF]->(p);

MATCH (p:Person {name: "@Merlin, Fred"})
MERGE (alias_freddy:Alias {rawValue: "Freddy", type: "nickname_variant"})
MERGE (alias_freddy)-[:ALIAS_OF]->(p);

MATCH (p:Person {name: "@Merlin, Fred"})
MERGE (alias_merlin:Alias {rawValue: "Merlin", type: "nickname_variant"})
MERGE (alias_merlin)-[:ALIAS_OF]->(p);

-- ============================================================================
-- COMMON NICKNAME PATTERNS (Add more as analysts discover them)
-- ============================================================================

-- Example: If we had William Eagle, add Bill aliases
-- MATCH (p:Person {name: "@Eagle, William"})
-- MERGE (alias_bill:Alias {rawValue: "Bill", type: "nickname_variant"})
-- MERGE (alias_bill)-[:ALIAS_OF]->(p);

-- Example: If we had Robert, add Bob aliases  
-- MATCH (p:Person {name: "@Robert"})
-- MERGE (alias_bob:Alias {rawValue: "Bob", type: "nickname_variant"})
-- MERGE (alias_bob)-[:ALIAS_OF]->(p);

-- ============================================================================
-- VALIDATION QUERY
-- ============================================================================

-- Show all manually created aliases
MATCH (alias:Alias {type: "nickname_variant"})-[:ALIAS_OF]->(p:Person)
RETURN 
    p.name as person,
    alias.rawValue as manual_alias,
    "Manual analyst knowledge" as source
ORDER BY p.name, alias.rawValue;