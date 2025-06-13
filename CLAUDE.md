# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Neo4j-based surveillance analytics POC that ingests communication session data (phone calls, SMS, emails) into a graph database for law enforcement investigations. It uses the POLE (Person, Object, Location, Event) schema and combines graph relationships with semantic search capabilities.

## Design Principles
- **LESS IS MORE**: Simplicity always wins over complexity. The most intelligent solutions are usually the simplest ones.

## Essential Commands

### Neo4j Setup
```bash
# Start Neo4j container with required plugins and procedures
docker run --name neo4j-sessions \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/Sup3rSecur3! \
  -e NEO4J_PLUGINS='["apoc","graph-data-science"]' \
  -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*,db.* \
  -e NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.*,db.* \
  -d neo4j:5.26.7-community

# Create schema (run first, before any data import)
cypher-shell -u neo4j -p Sup3rSecur3! -f scripts/cypher/01-schema.cypher
```

### Python Environment & Data Pipeline
```bash
# Setup Python environment
python -m venv .venv
source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
pip install -r scripts/python/requirements.txt

# Run data pipeline in order
python scripts/python/01-import-data.py  # Import NDJSON data (~2 min for 200 sessions)
python scripts/python/02-embed-text.py   # Generate text embeddings
python scripts/python/03-graphrag-demo.py  # Test GraphRAG queries

# Verify data import
cypher-shell -u neo4j -p Sup3rSecur3! -f scripts/cypher/02-sanity.cypher
```

### Query Execution
```bash
# Run investigative queries
cypher-shell -u neo4j -p Sup3rSecur3! -f queries/investigative.cypher

# Run evaluation test suite
cypher-shell -u neo4j -p Sup3rSecur3! -f queries/eval-suite.cypher
```

## Architecture & Key Design Patterns

### Graph Schema (Session-Centric POLE Model)
The system uses a session-centric approach where `Session` nodes are the central entities, connected to:
- `Person` nodes via phones/emails that `PARTICIPATED_IN` sessions
- `Phone`, `Email`, `Device` nodes representing communication endpoints
- `Content` nodes containing message text with embeddings

Key relationships follow law enforcement ontologies:
- `(:Phone)-[:PARTICIPATED_IN]->(:Session)` - Phone participation in sessions
- `(:Person)-[:USES]->(:Phone|Email)` - Person-to-identifier mapping
- `(:Session)-[:HAS_CONTENT]->(:Content)` - Session content linkage

### Data Processing Pipeline
1. **Schema Creation**: Establishes constraints, indexes, and vector index (384 dimensions)
2. **Data Import**: Processes NDJSON files, creating nodes/relationships while preserving raw data
3. **Embedding Generation**: Uses `sentence-transformers/all-MiniLM-L6-v2` for 384-dim embeddings
4. **GraphRAG Integration**: Enables semantic search via LangChain's Neo4j vector retriever

### Query Patterns
The system supports extensive query types documented in `evals/evaluation_tests.md`:
- Semantic search using vector embeddings
- Full-text search on content
- Time-based filtering
- Entity association analysis
- Communication pattern detection
- Multi-hop relationship traversal

### Important Implementation Details
- **Database credentials**: `neo4j` / `Sup3rSecur3!`
- **Vector dimensions**: 384 (matches all-MiniLM-L6-v2 model)
- **Batch processing**: 128 texts per embedding batch
- **Data format**: NDJSON with session/involvement/product structure
- **Content extraction**: Handles data URIs for text content

## Important Instructions
- NEVER use emojis in any files or documentation unless explicitly requested by the User
- Only create documentation files when explicitly requested
- Always prefer editing existing files to creating new ones