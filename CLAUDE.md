# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Neo4j-based surveillance analytics POC that ingests communication session data (phone calls, SMS, emails) into a graph database for law enforcement investigations. It uses the POLE (Person, Object, Location, Event) schema and combines graph relationships with semantic search capabilities.

## Design Principles
- **Less is More**: Simplicity always wins over complexity. The most intelligent solutions are usually the simplest ones.
- Follow **Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away** advice by Antoine de Saint-Exupéry.
- **Evals are tests for prompts**: Just as tests verify code, evals verify AI behavior. Write tests first, let them fail, then implement until they pass consistently (5+ runs for nondeterministic systems).
- **Tests are immutable**: Once written, tests define success. Implementation serves tests, not vice versa.

## Essential Commands

*For initial setup, see README.md. These are operational commands for development work.*

### Neo4j Operations
```bash
# Quick connection test
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3!

# Run schema validation
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/02-sanity.cypher

# Test vector search capability
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < queries/vector-search-verification.cypher
```

### Development Validation
```bash
# Activate environment and run data pipeline validation
source venv/bin/activate
python scripts/python/03-graphrag-demo.py  # Test GraphRAG queries

# Run evaluation suite (comprehensive business requirements test)
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

### Debugging Commands
```bash
# Check container status
docker ps | grep neo4j-sessions

# View Neo4j logs
docker logs neo4j-sessions

# Container restart (data loss - use for fresh start only)
docker stop neo4j-sessions && docker rm neo4j-sessions
```

## Neo4j GenAI Python Project

### Project Context
This project leverages Neo4j v5's latest Generative AI features including vector search, embeddings, and GraphRAG patterns.

### Key Technologies
- Neo4j v5.x with GDS (Graph Data Science) library
- Python async driver for Neo4j
- Vector embeddings and similarity search
- GraphRAG implementation

### Documentation References

#### Core Libraries
- [Python Driver](https://neo4j.com/docs/python-manual/current/)
- [Python Driver GitHub](https://github.com/neo4j/neo4j-python-driver)
- [GDS Python Client](https://neo4j.com/docs/graph-data-science-client/current/)
- [GDS Client API](https://neo4j.com/docs/graph-data-science-client/current/api/)
- [GDS GitHub](https://github.com/neo4j/graph-data-science)

#### GenAI & Vector Features
- [Cypher Vector Functions](https://neo4j.com/docs/cypher-manual/current/functions/vector/)
- [GenAI Integrations](https://neo4j.com/docs/cypher-manual/current/genai-integrations/)
- [Vector Indexes](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
- [Embeddings Tutorial](https://neo4j.com/docs/genai/tutorials/embeddings-vector-indexes/)

#### GraphRAG
- [Neo4j GraphRAG Python](https://neo4j.com/docs/neo4j-graphrag-python/current/)
- [GraphRAG Python API](https://neo4j.com/docs/neo4j-graphrag-python/current/api.html)

#### General Resources
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/introduction/cypher-neo4j/)
- [Graph Data Science Docs](https://neo4j.com/docs/graph-data-science/current/)

### Common Patterns
- Use async driver for all new features
- Vector dimension: 1536 (OpenAI compatible)
- Index naming: `{node_label}_embedding_index`


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

- **Data format**: NDJSON with session/involvement/product structure
- **Content extraction**: Handles data URIs for text content

## Important Instructions
- NEVER use emojis in any files or documentation unless explicitly requested by the User
- Only create documentation files when explicitly requested
- Always prefer editing existing files to creating new ones