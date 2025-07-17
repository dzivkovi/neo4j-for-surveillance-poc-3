/*
Content Search Enhancement - Participant Alias Integration
==========================================================

This script enhances content searchability by appending participant aliases
to content text, enabling natural language searches like "Freddy Miami" to
find content where "@Merlin, Fred" discusses Miami.

DEFENSIVE PROGRAMMING APPROACH:
- Validates each step before proceeding
- Handles edge cases (content without participants)
- Uses safe content modification patterns
- Includes rollback capability

Run AFTER: scripts/01-create-schema.sh, 02-import-sessions.py, 03-analyst-knowledge-aliases.cypher
Purpose: Enable intuitive searches without complex alias expansion queries

Business Value: Investigators can search "Freddy" and find all Fred's content
*/

-- ============================================================================
-- VALIDATION QUERIES (Run these first to verify system state)
-- ============================================================================

-- Check current system state
MATCH (c:Content) WHERE c.text IS NOT NULL RETURN count(c) as total_content;
MATCH (alias:Alias) RETURN count(alias) as total_aliases;
MATCH (alias:Alias {type: 'nickname_variant'}) RETURN count(alias) as manual_aliases;

-- ============================================================================
-- STEP 1: IDENTIFY CONTENT FOR ENHANCEMENT
-- ============================================================================

-- Show what will be enhanced (diagnostic query)
MATCH (c:Content)<-[:HAS_CONTENT]-(s:Session)<-[:PARTICIPATED_IN]-(device)<-[:USES]-(person:Person)
MATCH (person)<-[:ALIAS_OF]-(alias:Alias)
WHERE c.text IS NOT NULL 
  AND alias.type IN ['nickname', 'nickname_variant', 'msisdn']
  AND NOT c.text CONTAINS '[PARTICIPANTS:'  -- Don't re-enhance
WITH c, count(DISTINCT alias) as alias_count
RETURN count(DISTINCT c) as content_to_enhance,
       min(alias_count) as min_aliases,
       max(alias_count) as max_aliases,
       avg(alias_count) as avg_aliases;

-- ============================================================================
-- STEP 2: CONTENT ENHANCEMENT (MAIN OPERATION)
-- ============================================================================

-- Enhance content with participant aliases for improved searchability
MATCH (c:Content)<-[:HAS_CONTENT]-(s:Session)<-[:PARTICIPATED_IN]-(device)<-[:USES]-(person:Person)
MATCH (person)<-[:ALIAS_OF]-(alias:Alias)
WHERE c.text IS NOT NULL 
  AND alias.type IN ['nickname', 'nickname_variant', 'msisdn']
  AND NOT c.text CONTAINS '[PARTICIPANTS:'  -- Prevent double enhancement
WITH c, collect(DISTINCT alias.rawValue) as participant_aliases
WHERE size(participant_aliases) > 0
WITH c, apoc.text.join(participant_aliases, ' ') as alias_text
SET c.text = c.text + ' [PARTICIPANTS: ' + alias_text + ']',
    c.enhanced = true,
    c.enhancedAt = datetime();

-- ============================================================================
-- STEP 3: VALIDATION QUERIES (Verify enhancement worked)
-- ============================================================================

-- Check enhancement results
MATCH (c:Content) 
WHERE c.enhanced = true 
RETURN count(c) as enhanced_content,
       avg(size(c.text)) as avg_enhanced_size;

-- Show sample enhanced content
MATCH (c:Content) 
WHERE c.enhanced = true 
RETURN substring(c.text, 0, 200) + '...' as sample_enhanced_content
LIMIT 3;

-- ============================================================================
-- STEP 4: FUNCTIONAL TESTING
-- ============================================================================

-- Test that enhanced search now works
-- This should find content after enhancement
CALL db.index.fulltext.queryNodes('ContentFullText', 'Freddy AND Miami') 
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN count(s) as freddy_miami_results,
       avg(score) as avg_score;

-- ============================================================================
-- ROLLBACK PROCEDURE (Use if enhancement needs to be removed)
-- ============================================================================

-- UNCOMMENT BELOW TO ROLLBACK ENHANCEMENT:
/*
MATCH (c:Content) 
WHERE c.enhanced = true 
  AND c.text CONTAINS '[PARTICIPANTS:'
WITH c, split(c.text, ' [PARTICIPANTS:')[0] as original_text
SET c.text = original_text,
    c.enhanced = false
REMOVE c.enhancedAt;
*/

-- ============================================================================
-- MAINTENANCE QUERIES
-- ============================================================================

-- Show enhancement statistics
MATCH (c:Content) 
RETURN 
  count(CASE WHEN c.enhanced = true THEN 1 END) as enhanced_count,
  count(CASE WHEN c.enhanced = true THEN NULL ELSE 1 END) as unenhanced_count,
  count(c) as total_content;

-- Find content that might need re-enhancement (new aliases added)
MATCH (c:Content)<-[:HAS_CONTENT]-(s:Session)<-[:PARTICIPATED_IN]-(device)<-[:USES]-(person:Person)
MATCH (person)<-[:ALIAS_OF]-(alias:Alias {type: 'nickname_variant'})
WHERE c.enhanced = true 
  AND NOT c.text CONTAINS alias.rawValue
RETURN count(DISTINCT c) as content_needing_refresh;