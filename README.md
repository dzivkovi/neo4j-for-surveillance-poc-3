# Surveillance Graph Analytics Project

End-to-end sandbox that ingests *sessions.ndjson* (law-enforcement communication sessions) into Neo4j 5.x, builds full-text & vector indexes, and runs evaluation queries defined by client.

[![Project Board](https://img.shields.io/badge/Project%20Board-Kanban-blue)](https://github.com/users/dzivkovi/projects/1)

## Quick Start

```bash
# Set dataset name (defaults to "default" if not specified)
export DATASET=${DATASET:-default}
export NEO_NAME="neo4j-${DATASET}"

# 1. Start Neo4j container with required plugins
./run_neo4j.sh ${DATASET}  # Or just ./run_neo4j.sh for default

# 2. Create complete schema (constraints + indexes)
./01-create-schema.sh

# 3. Set up Python environment and import data
python -m venv venv
source venv/bin/activate
pip install -r scripts/python/requirements.txt

python scripts/python/02-import-sessions.py     # ~2 min for 265 sessions
python scripts/python/03-import-transcripts.py  # imports LanceDB transcripts

# 4. Generate embeddings for semantic search (requires OpenAI API key)
export NEO_NAME="neo4j-${DATASET}"
export OPENAI_API_KEY="sk-..."
./generate-embeddings.sh

# 5. Verify complete installation
python scripts/python/05-validate-setup.py

# 6. Apply analyst knowledge aliases (MANUAL - when needed)
# Use existing approach in scripts/cypher/03-analyst-knowledge-aliases.cypher
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/03-analyst-knowledge-aliases.cypher

# 7. Run evaluation suite
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

## Documentation

- **[Data Import](docs/import.md)** - Complete pipeline for data extraction and import
- **[Embedding Generation](docs/embedding-generation-guide.md)** - OpenAI embeddings using Neo4j GenAI
- **[Evaluation Framework](evals/README.md)** - 77-question validation suite with real-time progress
- **[Natural Language Queries](docs/mcp.md)** - Plain English database access via MCP
- **[Entity Resolution](docs/entity-resolution.md)** - Advanced identity linking
- **[Search Syntax](docs/lucene.md)** - Full-text search capabilities
- **[Case Study](docs/case-study.md)** - Real-world application example
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
./run_neo4j.sh default    # Switch to default dataset
./run_neo4j.sh bigdata    # Switch to bigdata dataset
./run_neo4j.sh clientA    # Switch to clientA dataset
```

### Container Operations
```bash
# Stop current container
docker stop ${NEO_NAME}

# Remove container (warning: data loss)
docker rm ${NEO_NAME}

# Data restoration after restart
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/01-schema.cypher
python scripts/python/01-import-data.py
python scripts/python/02-import-transcripts.py

# Test GenAI plugin installation
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! -c "SHOW FUNCTIONS YIELD name WHERE name CONTAINS 'genai' RETURN name"
```

### Dataset Snapshots (Optional)
```bash
# Create snapshot of current dataset
docker stop ${NEO_NAME}
docker commit ${NEO_NAME} ${NEO_NAME}:snap-$(date +%Y-%m-%d)
docker start ${NEO_NAME}
```

## For AI Assistants

See `CLAUDE.md` for project context and development guidelines.