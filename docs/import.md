# Data Import Guide

This guide covers the complete data import pipeline for the surveillance analytics system, from raw NDJSON files to a fully operational Neo4j graph database.

## Overview

The import process is designed around Unix principles of composable tools:

1. **Extract & Transform**: Prepare focused datasets from large surveillance files
2. **Import Base Structure**: Create nodes and relationships
3. **Enrich Metadata**: Add properties and enhance existing data

## Tools Overview

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `extract-sessions.py` | Transform NDJSON surveillance data | `sessions.ndjson` | Focused JSON |
| `01-import-data.py` | Create base graph structure | Extracted JSON | Neo4j nodes/relationships |
| `02-import-transcripts.py` | Add call transcripts | LanceDB export | Content nodes |

## 1. Session Data Extraction

The `extract-sessions.py` utility is your Swiss Army knife for preparing surveillance data.

### Basic Usage

```bash
# Preview what would be extracted (dry run)
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson --dry-run

# Extract default investigative fields
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson -o sessions-core.json

# Discover available fields
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson --list-fields

# Show current default fields
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson --show-defaults
```

### Default Field Set

Core investigative fields extracted by default:

- **Identity**: `sessionguid`, `displaytypeid`, `targetname`
- **Classification**: `sessiontype`, `classification`, `reviewstatus`  
- **Temporal**: `starttime`, `stoptime`, `durationinseconds`
- **Source**: `sourceid`

### Advanced Usage

```bash
# Preview extraction with custom fields (dry run)
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  --add fulltext --dry-run --sample 3

# Add large content fields
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  --add fulltext,previewcontent -o sessions-with-content.json

# Create minimal dataset for development
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  --remove targetname,sourceid -o sessions-minimal.json

# Size-limited export for AI analysis
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  --add fulltext --max-size 10 -o ai-analysis.json

# Extract only specific fields
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  --only sessionguid,sessiontype,durationinseconds -o telephony-analysis.json

# Pipe to downstream tools
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson | \
  ./scripts/python/01-import-data.py --stdin
```

### Field Categories

**✅ Default Fields**: Core investigative data (always included)
**📦 Large Fields**: Content-heavy fields (excluded by default):
- `products` - Complex nested structures
- `involvements` - Relationship arrays  
- `previewcontent` - Base64 encoded content
- `fulltext` - Complete text content
- `enrichment_` - AI/ML enrichments

**Debug Fields**: Useful for troubleshooting:
- `createddate`, `lastmodifydate`, `decodestate`

### Data Statistics

The tool provides detailed statistics about your dataset:

```bash
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson --stats-only
```

Example output:
```
📊 Extraction Statistics:
   Total records read: 265
   Output size: 0.1 MB

📞 Session Types:
   Telephony: 42
   Messaging: 159
   Email: 50
   Entity Report: 10

🏷️  Classifications:
   Pertinent: 65
   Non-Pertinent: 108
   Unknown: 90
```

## 2. Base Graph Import

Import the core graph structure with nodes and relationships:

```bash
# Import extracted session data
python scripts/01-import-data.py sessions-core.json

# Import with progress monitoring
python scripts/01-import-data.py sessions-core.json --verbose
```

This creates:
- **Session nodes** with basic properties
- **Person nodes** linked to identifiers
- **Phone/Email nodes** with participation relationships
- **Location nodes** with geographic data

## 3. Transcript Integration

Add call transcripts from LanceDB system:

```bash
# Export transcripts from LanceDB
cd /path/to/lancedb-project
python export_for_neo4j.py -o transcripts.json

# Import transcripts into Neo4j
cd /path/to/neo4j-project  
python scripts/02-import-transcripts.py transcripts.json
```

This creates:
- **Content nodes** with transcript text
- **HAS_CONTENT relationships** linking sessions to transcripts
- **Full-text indexes** for content search


## Complete Workflow Examples

### Development Setup (Fast, Minimal)

```bash
# Create minimal dataset
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  --remove products,involvements,fulltext \
  --max-size 5 -o dev-sessions.json

# Quick import
python scripts/01-import-data.py dev-sessions.json
python scripts/02-import-transcripts.py transcripts.json
```

### Production Setup (Complete)

```bash
# Full extraction with metadata
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  -o sessions-full.json

# Complete import pipeline
python scripts/01-import-data.py sessions-full.json
python scripts/02-import-transcripts.py transcripts.json
```

### Analysis Export (AI-Friendly)

```bash
# Create lightweight dataset for analysis
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson \
  --add fulltext \
  --remove products,involvements,previewcontent \
  --max-size 25 -o analysis-export.json
```

## Data Format Specifications

### Extracted Session Format

```json
{
  "sessionguid": "d4f60749-2577-49eb-be5d-1977c84aa2a2",
  "sessiontype": "Telephony",
  "classification": "Pertinent", 
  "reviewstatus": "Completed",
  "starttime": "2020-02-07T12:53:27.000Z",
  "durationinseconds": 11,
  "displaytypeid": "telephony",
  "sourceid": "Local 3.9",
  "targetname": "@Eagles Maintenance and Landscaping"
}
```

### Transcript Format

```json
{
  "session_id": "d4f60749-2577-49eb-be5d-1977c84aa2a2",
  "text": "Full transcript text...",
  "chunk_count": 3,
  "char_count": 1247,
  "session_type": "Telephony",
  "content_type": "audio/wav"
}
```

## Troubleshooting

### Common Issues

**"Field not found" errors**:
```bash
# Check available fields first
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson --list-fields
```

**Large file processing**:
```bash
# Use size limits for testing
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson --max-size 1 -o test.json
```

**Memory issues**:
```bash
# Process in compact mode
./scripts/extract-sessions.py data/whiskey-jack/sessions.ndjson --compact -o output.json
```

### Validation

Verify your extracted data:

```bash
# Check session types
jq '[.[] | .sessiontype] | group_by(.) | map({type: .[0], count: length})' sessions-core.json

# Check for missing GUIDs
jq '.[] | select(.sessionguid == null)' sessions-core.json

# Validate telephony durations
jq '.[] | select(.sessiontype == "Telephony" and .durationinseconds > 0)' sessions-core.json
```

## Performance Notes

- **Field selection**: Excluding large fields (`products`, `fulltext`) reduces file size by 80-90%
- **Size limits**: Use `--max-size` for testing and AI exports
- **Compact output**: Use `--compact` for production pipelines
- **Streaming**: All tools support stdin/stdout for pipeline composition

## Security Considerations

- **Data minimization**: Extract only fields needed for your analysis
- **Size limits**: Prevent accidental creation of massive files
- **Field filtering**: Remove sensitive fields from shared exports
- **Audit trail**: All tools log their operations for compliance

The extraction tool provides the foundation for flexible, secure data preparation while maintaining the Unix philosophy of simple, composable tools.

## Running Cypher Queries in Neo4j Docker Container


## Method 1: Execute cypher-shell inside the container

```bash
# Basic syntax
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3!

# Run a single query
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! "MATCH (n) RETURN count(n);"

# Run a query file
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < queries/investigative.cypher

# Run with formatted output
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain "MATCH (s:Session) RETURN keys(s) LIMIT 1;"
```

## Method 2: Interactive shell session

```bash
# Start an interactive cypher-shell session
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3!

# Once inside, you can run queries:
neo4j@neo4j> MATCH (n) RETURN count(n);
neo4j@neo4j> :exit
```

## Method 3: Using bash heredoc for multi-line queries

```bash
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<'EOF'
MATCH (s:Session)
RETURN keys(s) as properties
LIMIT 1;
EOF
```

## Method 4: Copy and execute files

```bash
# Copy a query file into the container first
docker cp queries/practical-investigation-queries.cypher ${NEO_NAME}:/tmp/

# Then execute it
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! -f /tmp/practical-investigation-queries.cypher
```

## Useful Options

- `--format plain` - Plain text output (no boxes)
- `--format json` - JSON output
- `--format verbose` - Detailed output with execution plans
- `-f filename` - Execute queries from a file
- `--non-interactive` - Don't prompt for input

## Example: Check Session Properties

```bash
# Let's check what properties Session nodes actually have
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! --format plain "MATCH (s:Session) RETURN DISTINCT keys(s) as properties LIMIT 5;"
```
