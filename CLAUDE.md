# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Neo4j-based surveillance analytics POC that ingests communication session data (phone calls, SMS, emails) into a graph database for law enforcement investigations. It uses the POLE (Person, Object, Location, Event) schema and combines graph relationships with semantic search capabilities.

## Design Principles
- Follow **Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away** advice by Antoine de Saint-Exupéry.
- **Optimize for User Interaction Pattern**: Before structuring anything, ask "How will users interact with this?" Browsing/scanning tasks favor flat layouts that minimize cognitive load; direct navigation tasks can use logical hierarchy.
- **Defensive Programming**: Test everything, validate all assumptions, never rush implementation. Every query must be tested with MCP server before documentation. Expect failures and plan for them.
- **Documentation-First**: Always check latest official docs before implementing. Technology changes faster than training data or existing code.
- **Evals are tests for prompts**: Just as tests verify code, evals verify AI behavior. Write tests first, let them fail, then implement until they pass consistently (5+ runs for nondeterministic systems).
- **Tests are immutable**: Once written, tests define success. Implementation serves tests, not vice versa.

## Essential Commands

*For initial setup, see README.md. These are operational commands for development work.*

### Neo4j Operations
```bash
# Quick connection test for development
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3!

# Run schema validation
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/02-sanity.cypher

# Test vector search capability
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < queries/vector-search-verification.cypher
```

### Development Validation
```bash
# Test GraphRAG queries after environment setup
source venv/bin/activate && python scripts/python/03-graphrag-demo.py

# Run comprehensive business requirements test
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

### Debugging Commands
```bash
# Check container status
docker ps | grep neo4j-sessions

# View Neo4j logs for troubleshooting
docker logs neo4j-sessions

# Container restart (data loss - use for fresh start only)
docker stop neo4j-sessions && docker rm neo4j-sessions
```

### Evaluation System Commands
```bash
# Interactive evaluation development (the "dance" approach)
PYTHONPATH=. python scripts/python/neo4j_query_executor.py eval EVAL-27

# Batch confidence processing for auto-promotion
PYTHONPATH=. python scripts/python/neo4j_query_executor.py confidence --batch

# Update progress dashboard
python scripts/python/evaluation_harness.py dashboard

# Run comprehensive validation suite
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/validation-suite.cypher
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
- Vector dimensions: 1536 (current OpenAI text-embedding-3-small)
- Index naming: `{node_label}_embedding_index`

## Documentation-First Development
**IMPORTANT**: Technology evolves rapidly. When implementing any feature:
1. ALWAYS check official documentation first (links provided above)
2. Compare with existing code patterns second
3. Explain any differences between docs and local implementation
4. Trust latest documentation over:
   - My training data (likely outdated)
   - Existing codebase (may be legacy)
   - Examples in this file (may be from earlier versions)

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
1. **Schema Creation**: Establishes constraints, indexes, and vector index (1536 dimensions)
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
- **Database credentials**: `neo4j` / `Sup3rSecur3!` (intentionally hardcoded for local POC)

- **Data format**: NDJSON with session/involvement/product structure
- **Content extraction**: Handles data URIs for text content

## Important Instructions
- **NEVER sign commits or changes as Claude/AI** - use standard git authorship only
- NEVER use emojis in any files or documentation unless explicitly requested by the User
- Only create documentation files when explicitly requested
- Always prefer editing existing files to creating new ones
- NEVER write Cypher queries into files without first validating them using the MCP Neo4j server
- ALWAYS test Cypher queries with mcp__neo4j__read_neo4j_cypher before documenting them

## ⚠️ Critical Terminology for Client Communication
- **"Failed" tests ≠ broken queries** - they are unprocessed tests awaiting confidence assessment
- **96.4% of "failed" tests work correctly** when properly evaluated (validated 2025-07-03)
- Use clear language: "needs assessment" not "failed" when discussing with clients
- The evaluation system has high reliability - most issues are process/assessment related, not technical failures

## Defensive Programming Requirements
**MANDATORY**: Follow these validation steps after EVERY code change:

### After Each Edit:
1. **Search for related occurrences**: Use `rg` to find ALL instances of what you're changing
2. **Test the specific change**: Run focused tests on the modified functionality
3. **Check for side effects**: Verify nothing else broke

### Before ANY Commit:
1. **Run comprehensive search**: `rg <pattern>` to verify all occurrences were updated
2. **Run test suite**: `python -m pytest tests/ -v` (or relevant test command)
3. **Test functionality**: Actually execute the code/queries you modified
4. **List what you validated**: Tell the user exactly what you tested

### Use TodoWrite for Complex Changes:
- Create a checklist of ALL files to modify
- Mark each as "in_progress" while working
- Test after each completion
- Only mark "completed" after validation passes

### Example Validation Pattern:
```bash
# After editing Python files
python -m pytest tests/test_affected_module.py -v
rg "old_pattern" .  # Should return nothing

# After editing Cypher queries
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < modified_query.cypher

# After editing multiple files
for file in $(git diff --name-only); do
    echo "Validating $file..."
    # Run appropriate validation
done
```

### NEVER:
- Declare success without testing
- Commit without running validation
- Say "all occurrences fixed" without using `rg` to verify
- Assume one fix applies everywhere without checking
