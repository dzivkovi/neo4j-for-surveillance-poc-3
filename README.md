# Surveillance Graph Analytics Project

End-to-end sandbox that ingests *sessions.ndjson* (law-enforcement communication sessions) into Neo4j 5.x, builds full-text & vector indexes, and runs evaluation queries defined by client.

[![Project Board](https://img.shields.io/badge/Project%20Board-Kanban-blue)](https://github.com/users/dzivkovi/projects/1)

## Quick Start

```bash
# 1. Start Neo4j container with required plugins
docker run --name neo4j-sessions \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/Sup3rSecur3! \
  -e NEO4J_PLUGINS='["apoc","graph-data-science"]' \
  -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*,db.* \
  -e NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.*,db.* \
  -d neo4j:5.26.7-community

# 2. Create schema and indexes
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/01-schema.cypher

# 3. Set up Python environment and import data
python -m venv venv
source venv/bin/activate
pip install -r scripts/python/requirements.txt

python scripts/python/01-import-data.py         # ~2 min for 200 sessions
python scripts/python/02-import-transcripts.py  # imports LanceDB transcripts

# 4. Verify installation
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

## Documentation

- **[Data Import](docs/import.md)** - Complete pipeline for data extraction and import
- **[Evaluation Framework](docs/evaluations.md)** - 77-question validation suite
- **[Natural Language Queries](docs/mcp.md)** - Plain English database access via MCP
- **[Entity Resolution](docs/entity-resolution.md)** - Advanced identity linking
- **[Search Syntax](docs/lucene.md)** - Full-text search capabilities
- **[Case Study](docs/case-study.md)** - Real-world application example
- **[GitHub Projects](docs/kanban.md)** - Task tracking and workflow
- **[Claude Automation](docs/claude-automation.md)** - AI-powered PR reviews

## Core Capabilities

**📊 Current Status**: 37/77 evaluation tests passing (48%)

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
- **Vector search** - Neo4j 5.11+ with sentence-transformers (384 dims)
- **GraphRAG ready** - LangChain integration for AI-powered analysis

## Container Management

```bash
# Stop and restart (data loss warning)
docker stop neo4j-sessions && docker rm neo4j-sessions
# Then re-run Quick Start steps

# Data restoration after restart
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/01-schema.cypher
python scripts/python/01-import-data.py
python scripts/python/02-import-transcripts.py
```

## For AI Assistants

See `CLAUDE.md` for project context and development guidelines.