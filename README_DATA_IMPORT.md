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
| `enrich-metadata.py` | Add session properties | Original NDJSON | Enhanced Session nodes |

## 1. Session Data Extraction

The `extract-sessions.py` utility is your Swiss Army knife for preparing surveillance data.

### Basic Usage

```bash
# Preview what would be extracted (dry run)
./scripts/python/extract-sessions.py data/sessions.ndjson --dry-run

# Extract default investigative fields
./scripts/python/extract-sessions.py data/sessions.ndjson -o sessions-core.json

# Discover available fields
./scripts/python/extract-sessions.py data/sessions.ndjson --list-fields

# Show current default fields
./scripts/python/extract-sessions.py data/sessions.ndjson --show-defaults
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
./scripts/python/extract-sessions.py data/sessions.ndjson \
  --add fulltext --dry-run --sample 3

# Add large content fields
./scripts/python/extract-sessions.py data/sessions.ndjson \
  --add fulltext,previewcontent -o sessions-with-content.json

# Create minimal dataset for development
./scripts/python/extract-sessions.py data/sessions.ndjson \
  --remove targetname,sourceid -o sessions-minimal.json

# Size-limited export for AI analysis
./scripts/python/extract-sessions.py data/sessions.ndjson \
  --add fulltext --max-size 10 -o ai-analysis.json

# Extract only specific fields
./scripts/python/extract-sessions.py data/sessions.ndjson \
  --only sessionguid,sessiontype,durationinseconds -o telephony-analysis.json

# Pipe to downstream tools
./scripts/python/extract-sessions.py data/sessions.ndjson | \
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
./scripts/python/extract-sessions.py data/sessions.ndjson --stats-only
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
python scripts/python/01-import-data.py sessions-core.json

# Import with progress monitoring
python scripts/python/01-import-data.py sessions-core.json --verbose
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
python scripts/python/02-import-transcripts.py transcripts.json
```

This creates:
- **Content nodes** with transcript text
- **HAS_CONTENT relationships** linking sessions to transcripts
- **Full-text indexes** for content search

## 4. Metadata Enrichment

> **Note**: This tool will be created to add missing session metadata to existing graphs.

```bash
# Enrich existing sessions with metadata
python scripts/python/enrich-metadata.py data/sessions.ndjson

# Selective enrichment
python scripts/python/enrich-metadata.py data/sessions.ndjson \
  --only sessionType,durationInSeconds,classification
```

## Complete Workflow Examples

### Development Setup (Fast, Minimal)

```bash
# Create minimal dataset
./scripts/python/extract-sessions.py data/sessions.ndjson \
  --remove products,involvements,fulltext \
  --max-size 5 -o dev-sessions.json

# Quick import
python scripts/python/01-import-data.py dev-sessions.json
python scripts/python/02-import-transcripts.py transcripts.json
```

### Production Setup (Complete)

```bash
# Full extraction with metadata
./scripts/python/extract-sessions.py data/sessions.ndjson \
  -o sessions-full.json

# Complete import pipeline
python scripts/python/01-import-data.py sessions-full.json
python scripts/python/02-import-transcripts.py transcripts.json
python scripts/python/enrich-metadata.py data/sessions.ndjson
```

### Analysis Export (AI-Friendly)

```bash
# Create lightweight dataset for analysis
./scripts/python/extract-sessions.py data/sessions.ndjson \
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
./scripts/python/extract-sessions.py data/sessions.ndjson --list-fields
```

**Large file processing**:
```bash
# Use size limits for testing
./scripts/python/extract-sessions.py data/sessions.ndjson --max-size 1 -o test.json
```

**Memory issues**:
```bash
# Process in compact mode
./scripts/python/extract-sessions.py data/sessions.ndjson --compact -o output.json
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
