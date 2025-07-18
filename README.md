# Surveillance Graph Analytics Project

End-to-end sandbox that ingests *sessions.ndjson* (law-enforcement communication sessions) into Neo4j 5.x, builds full-text & vector indexes, and runs evaluation queries defined by client.

[![Project Board](https://img.shields.io/badge/Project%20Board-Kanban-blue)](https://github.com/users/dzivkovi/projects/1)

## Quick Start

```bash
# Set dataset name (defaults to "default" if not specified)
export DATASET=${DATASET:-default}
export NEO_NAME="neo4j-${DATASET}"

# 1. Start Neo4j container with required plugins
./scripts/run-neo4j.sh ${DATASET}  # Or just ./scripts/run-neo4j.sh for default

# 2. Create complete schema (constraints + indexes)
scripts/01-create-schema.sh

# 3. Set up Python environment and import data
python -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt

python scripts/02-import-sessions.py --dataset ${DATASET}      # ~2 min for 265 sessions
python scripts/03-decode-sms-content.py                        # extract SMS from base64
python scripts/04-import-additional-content.py                 # import police reports, social media, call transcripts
python scripts/05-import-transcripts.py --dataset ${DATASET}   # imports LanceDB transcripts

# 4. Generate embeddings for semantic search (requires OpenAI API key)
export NEO_NAME="neo4j-${DATASET}"
export OPENAI_API_KEY="sk-..."
./scripts/06-generate-embeddings.sh

# 5. Verify complete installation
python scripts/07-validate-setup.py

# 6. Apply analyst knowledge aliases (MANUAL - when needed)
# Use existing approach in scripts/03-analyst-knowledge-aliases.cypher
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/03-analyst-knowledge-aliases.cypher

# 7. Run evaluation suite
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

## Test Results & Demo

🌐 **[Live Demo Site](https://dzivkovi.github.io/neo4j-for-surveillance-poc-3/)** - Professional test results dashboard

📋 **[Automated Test Suite](tests/README.md)** - 55 EVAL queries with 71% success rate

## Documentation

### Schema & Architecture
- **[Graph Schema Guide](docs/graph-schema-guide.md)** - Complete Neo4j schema documentation with POLE model
- **[Schema Diagram](docs/neo4j-graph-schema.mmd)** - Visual entity-relationship diagram

### Data Pipeline
- **[Data Import](docs/import.md)** - Complete pipeline for data extraction and import
- **[Embedding Generation](docs/embedding-generation-guide.md)** - OpenAI embeddings using Neo4j GenAI
- **[Entity Resolution](docs/entity-resolution.md)** - Advanced identity linking

### Query & Analysis
- **[Evaluation Framework](evals/README.md)** - 77-question validation suite with real-time progress
- **[Natural Language Queries](docs/mcp.md)** - Plain English database access via MCP
- **[Search Syntax](docs/lucene.md)** - Full-text search capabilities
- **[Case Study](docs/case-study.md)** - Real-world application example

### Development & Testing
- **[Test Reports Guide](docs/pytest-reports-guide.md)** - HTML report generation and viewing
- **[GitHub Projects](docs/kanban.md)** - Task tracking and workflow
- **[Claude Automation](docs/claude-automation.md)** - AI-powered PR reviews
- **[Git Workflow Guide](docs/git-workflow-rescue.md)** - Rescue guide for retroactive design-issue-work cycle

## Core Capabilities

**📊 Current Status**: 56/77 evaluation tests passing (73%) ✅

> **Note**: Current breakdown - 56 passed, 2 failed, 1 under review, 18 blocked (framework features). The system demonstrates 94% success rate on core Neo4j functionality (56/59 relevant tests).

### Entity Tracking
- Multi-identifier resolution: "What phones is Kenzie using?" → 24 numbers
- Device intelligence: "Who used IMEI 359847107165930?" → William Eagle (75), Ted Dowitcher (1)
- Communication patterns: "How does Kenzie contact Owen?" → SMS (24), Telephony (7)

### Content Analysis
- Evidence discovery: "sago palms references?" → 5 matches with relevance scoring
- Cross-entity search: "Has Kenzie mentioned a shed?" → 7 references found
- Travel intelligence: "Does Fred discuss travel?" → Miami meetings Feb 9-14

### Network Analysis
- Association mapping: "William Eagle's top contacts?" → Richard Eagle (29), Fred Merlin (18)
- Multi-hop traversal: Relationship chains up to 3 degrees
- Time-based filtering: Morning sessions, pertinent classifications

## Query Collections

- `queries/eval-suite.cypher` - Business requirements validation
- `queries/investigative.cypher` - Law enforcement use cases  
- `queries/network-visualizations.cypher` - Communication network graphs
- `queries/vector-search-verification.cypher` - Semantic search testing

## Design Principles

- **Session-centric POLE schema** - Direct NDJSON→graph mapping matching law enforcement ontologies
- **Immutable raw data** - Clear provenance and reproducibility
- **Semantic search** - OpenAI embeddings (1536 dims) with Neo4j vector indexes
- **GenAI integration** - Built-in Neo4j GenAI functions for embedding generation
- **GraphRAG ready** - LangChain integration for AI-powered analysis

## Testing

```bash
# Run unit tests
source venv/bin/activate
python -m pytest tests/ -v

# Run business validation queries  
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

## Container Management

### Dataset Switching
```bash
# Quick dataset switching (< 10 seconds)
./scripts/run-neo4j.sh default          # Switch to default dataset
./scripts/run-neo4j.sh whiskey-jack     # Switch to whiskey-jack dataset
./scripts/run-neo4j.sh bigdata          # Switch to bigdata dataset
```

### Container Operations
```bash
# Stop current container
docker stop ${NEO_NAME}

# Remove container (warning: data loss)
docker rm ${NEO_NAME}

# Data restoration after restart
scripts/01-create-schema.sh
python scripts/02-import-sessions.py --dataset ${DATASET}
python scripts/03-decode-sms-content.py
python scripts/04-import-additional-content.py
python scripts/05-import-transcripts.py --dataset ${DATASET}

# Test GenAI plugin installation
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! -c "SHOW FUNCTIONS YIELD name WHERE name CONTAINS 'genai' RETURN name"
```

### Database Backup and Restore

```bash
# Create portable database dump (recommended for case data)
./scripts/backup-neo4j.sh ${DATASET}

# Creates timestamped dump file:
# data/${DATASET}/neo4j-database-YYYY-MM-DD_HHMMSS.dump

# To restore from dump:
docker stop neo4j-${DATASET}
docker run --rm \
  --volumes-from neo4j-${DATASET} \
  -v $(pwd)/path/to/dump.file:/dump.file \
  neo4j:5.26.7-community \
  neo4j-admin database load neo4j --from-stdin --overwrite-destination < /dump.file
docker start neo4j-${DATASET}
```

**Note**: Database dumps are portable across Neo4j 5.x instances and ideal for sharing case data with clients.

## For AI Assistants

See `CLAUDE.md` for project context and development guidelines.