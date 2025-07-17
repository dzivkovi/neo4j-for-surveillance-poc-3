# Complete Neo4j Setup Guide

This guide ensures you can recreate the exact Neo4j configuration from scratch, matching the original neo4j-sessions setup.

## Prerequisites

- Docker installed and running
- OpenAI API key (for embedding generation)
- Python 3.8+ installed

## Step-by-Step Setup

### 1. Start Neo4j Container

```bash
# Set your dataset name (or use default)
export DATASET="default"
./scripts/run-neo4j.sh $DATASET
```

This creates a container named `neo4j-${DATASET}` with GenAI plugin enabled.

### 2. Create Initial Schema

```bash
export NEO_NAME="neo4j-${DATASET}"
scripts/01-create-schema.sh
```

This creates the base constraints and indexes.

### 3. Import Session Data

```bash
python scripts/02-import-sessions.py
```

This imports session data from the NDJSON files into Neo4j.

### 4. Set Up Python Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r scripts/requirements.txt
```

### 5. Import Data

```bash
# Import session data
python scripts/01-import-data.py

# Import transcripts from LanceDB
python scripts/02-import-transcripts.py
```

### 6. Generate Embeddings

```bash
export OPENAI_API_KEY="sk-..."
./scripts/04-generate-embeddings.sh
```

This generates 1536-dimensional OpenAI embeddings for all Content nodes.

### 7. Verify Setup

```bash
python scripts/verify-setup.py
```

This checks that all constraints, indexes, and embeddings are properly configured.

## Expected Final State

After completing all steps, you should have:

### Constraints (5 total)
- `session_guid` on Session.sessionguid
- `phone_number` on Phone.number
- `email_addr` on Email.email
- `device_imei` on Device.imei
- `alias_raw_unique` on Alias.rawValue

### Indexes (8+ additional)
- **Full-text**: ContentFullText, AliasText
- **Vector**: ContentVectorIndex (1536 dimensions)
- **Spatial**: locationGeo (POINT type)
- **Range**: sessionDuration, session_createddate, session_sessiontype, person_name
- **Automatic**: LOOKUP indexes and backing indexes for constraints

### Node Counts (approximate)
- Session: 265
- Content: 215+ (with embeddings)
- Person: 40
- Phone: 24
- Email: 18
- Device: 17
- Location: 41
- Alias: 89+

### Key Properties
- All Content nodes with text have 1536-dimensional embeddings
- Sessions have duration, classification, and other metadata
- Alias nodes link identifiers to Person nodes

## Troubleshooting

### Constraints Not Created
If constraints aren't created, run them individually:
```bash
echo "CREATE CONSTRAINT session_guid IF NOT EXISTS FOR (s:Session) REQUIRE s.sessionguid IS UNIQUE;" | docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3!
```

### Embeddings Missing
If embeddings are missing, check:
1. OPENAI_API_KEY is set correctly
2. Neo4j GenAI plugin is enabled
3. Run verify-setup.py to see specific issues

### Wrong Property Names
The schema uses these exact property names:
- `sessionguid` (NOT session_guid)
- `number` (NOT phone_number)
- `email` (NOT email_address)
- `imei` (NOT device_id)

## Validation Queries

Check your setup with these queries:

```cypher
// Count constraints
SHOW CONSTRAINTS;

// Count indexes by type
SHOW INDEXES
YIELD type, collect(name) as names
RETURN type, size(names) as count, names;

// Check embeddings
MATCH (c:Content)
RETURN 
    count(c) as total,
    count(c.embedding) as with_embeddings,
    count(CASE WHEN size(c.embedding) = 1536 THEN 1 END) as correct_dims;
```