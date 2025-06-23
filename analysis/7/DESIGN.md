# Feature #7: Transcripts & Lucene Search Implementation Design

## Executive Summary

This document consolidates the design decisions for implementing GitHub issue #7: "Reload communication sessions with transcripts, aliases, and locations with full Lucene/BM25 search capabilities." The design leverages Neo4j's built-in Lucene full-text search, avoiding vector embeddings while maintaining POLE compliance and answering all 77 evaluation questions.

## Design Principles

1. **Less is More**: Add only what's needed to answer evaluation questions
2. **No Vectors Yet**: Use Neo4j's built-in Lucene full-text search with BM25 ranking
3. **Reuse Existing Schema**: Content nodes already exist; just populate them
4. **POLE Compliance**: Maintain Person, Object, Location, Event structure

## Current State Analysis

### What We Already Have
- `:Session`, `:Person`, `:Phone`, `:Email`, `:Device`, `:Location` nodes
- `:Content` nodes with `text` property for storing transcripts/messages
- `ContentFullText` full-text index on `Content.text`
- Vector index (commented out - not needed for this phase)
- Base64-encoded SMS content in `Session.previewcontent`
- Email content already imported into Content nodes

### What's Missing
- Phone call transcripts from LanceDB
- Alias nodes for phone numbers, IMEIs, nicknames
- Location data properly linked
- Metadata properties: duration, classification, reviewStatus, etc.
- Additional indexes for efficient queries

## Implementation Plan

### 1. Schema Additions (01-schema.cypher)

```cypher
-- Append to existing schema file:

-- Drop existing location index (wrong type)
DROP INDEX location_coord IF EXISTS;

-- Point index for spatial queries
CREATE POINT INDEX locationGeo IF NOT EXISTS
FOR (l:Location) ON (l.geo);

-- Range index for temporal/duration queries  
CREATE RANGE INDEX sessionDuration IF NOT EXISTS
FOR (s:Session) ON (s.durationinseconds);

-- Full-text index for alias searches
CREATE FULLTEXT INDEX AliasText IF NOT EXISTS
FOR (a:Alias) ON EACH [a.rawValue];

-- Uniqueness constraint for aliases
CREATE CONSTRAINT alias_raw_unique IF NOT EXISTS
FOR (a:Alias) REQUIRE a.rawValue IS UNIQUE;
```

### 2. Enhanced Metadata Import (01-import-data.py)

Add these properties to Session nodes:
- `classification` - default "Unknown"
- `reviewStatus` - default "Unknown"
- `application` - from linename, default "Unknown"
- `languages` (list) - from multidetectedlanguages, default []
- `contentType` - from previewcontenttype
- `hasAudio` (boolean) - true if contentType starts with "audio"

### 3. Alias Node Pattern

Create `:Alias` nodes for all identifiers:
```cypher
(:Alias {rawValue: '+17205088591', type: 'msisdn'})
  -[:ALIAS_OF]->(:Person {personId: 'uuid'})
  
(:Alias {rawValue: 'Freddy', type: 'nickname'})
  -[:ALIAS_OF]->(:Person)
```

Types: 'msisdn', 'imei', 'email', 'nickname'

### 4. Transcript Import Script (02-import-transcripts.py)

New script to:
1. Connect to LanceDB
2. Aggregate transcript chunks by session_id
3. Create Content nodes with full text
4. Link to existing Session nodes via HAS_CONTENT

```python
# Core logic:
sql = """
SELECT session_id, STRING_AGG(text, ' ') AS full_text
FROM (SELECT * FROM lance ORDER BY timestamp, chunk_id)
GROUP BY session_id
"""
# Then create Content nodes...
```

### 5. Updated Sanity Check (02-sanity.cypher)

Enhance validation to show:
- Node/relationship counts
- Index status verification
- Sample transcripts (truncated)
- Alias coverage
- Duration statistics
- Location presence
- Audio vs non-audio breakdown

## Query Capabilities

### What We Can Answer with This Design

**Full-Text Search (10+ evaluation questions)**
- "sago palms", "shed", "murder", "cherry blasters" etc.
- Fuzzy search: `fred~` matches fred, freddy, fredy
- Wildcards: `sag*` matches sago, sagos
- Phrase search: `"bring docs"~3` (within 3 words)

**Alias-Based Queries (eval #68-77)**
- What phone numbers is Kenzie using?
- Which IMEIs are associated with phone X?
- Who has been using device with IMEI Y?

**Temporal Queries**
- Sessions longer than 60 seconds
- Morning sessions (using startTime)
- Recent 48-hour activity

**Location Queries**
- Last known location of person X
- Sessions within 10km of location Y

### What We Cannot Answer (Yet)
- "Travel plans" (requires semantic search or synonyms)
- Origin vs destination for calls (only single location)
- Complex summarization (needs aggregation logic)

## Implementation Steps

### Step 1: Schema Updates (scripts/cypher/01-schema.cypher)
```cypher
-- Append these to existing schema file:
DROP INDEX location_coord IF EXISTS;
CREATE POINT INDEX locationGeo IF NOT EXISTS FOR (l:Location) ON (l.geo);
CREATE RANGE INDEX sessionDuration IF NOT EXISTS FOR (s:Session) ON (s.durationinseconds);
CREATE FULLTEXT INDEX AliasText IF NOT EXISTS FOR (a:Alias) ON EACH [a.rawValue];
CREATE CONSTRAINT alias_raw_unique IF NOT EXISTS FOR (a:Alias) REQUIRE a.rawValue IS UNIQUE;
```

### Step 2: Update Import Script (scripts/python/01-import-data.py)
Add alias creation logic for each involvement

### Step 3: Create Transcript Import (scripts/python/02-import-transcripts.py)  
Aggregate LanceDB chunks by session_id

### Step 4: Update Validation (scripts/cypher/02-sanity.cypher)
Add checks for aliases, transcripts, indexes

### Step 5: Create Tests (tests/test_issue_7.py)
3 pytest tests to verify implementation

## Testing Strategy

Three minimal tests to verify:
```python
def test_content_present(sess):
    # Verify transcripts loaded
    
def test_alias_search(sess):
    # Verify phone aliases searchable
    
def test_duration(sess):
    # Verify duration property populated
```

## Migration Notes

- No data model changes required
- All additions are backward compatible
- Existing data remains intact
- Can be run incrementally

## Key Design Decisions

1. **Single Location per Session**: Treat as "best available device location" rather than origin/destination split
2. **Alias Nodes vs Properties**: Separate nodes allow multiple identifiers per person and enable fuzzy matching
3. **No Alias Merging Yet**: Import all aliases as-is; merge duplicates in post-processing phase
4. **Content Reuse**: Store all text (calls, SMS, emails) in same Content.text property
5. **Lucene Over Vectors**: Sufficient for literal/fuzzy matching required by evaluation tests

## Performance Considerations

- Alias uniqueness constraint speeds MERGE operations
- Range index on duration enables efficient inequality queries
- Point index on location accelerates distance calculations
- Full-text indexes use Lucene's BM25 scoring automatically

## Future Extensions (Not in Scope)

- Vector embeddings for semantic search
- Origin/destination split for calls
- Alias resolution/merging logic
- Multi-language analyzers
- Chunking for large documents

## Conclusion

This design provides the minimal set of changes needed to:
- Import all available text content (calls, SMS, emails)
- Enable fuzzy/wildcard text search via Lucene
- Support identifier-based queries (phone, IMEI, email)
- Answer location and duration-based questions
- Maintain POLE compliance
- Keep the solution simple and maintainable

Total implementation effort: ~4 hours
Risk: Low (all using standard Neo4j features)