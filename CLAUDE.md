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
- **Use `rg` first**: ALWAYS use `rg` (ripgrep) for searching before trying `grep` or `find` combinations. It's faster and better.
- **cypher-shell NEVER supports `-c` flag**: ALWAYS use `echo "QUERY" | docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3!` pattern.

## Task Planning
- **Complex tasks (3+ steps)**: Use TodoWrite to track progress
- **Simple tasks**: Execute directly without todo overhead

## Essential Commands

*For initial setup, see README.md. These are operational commands for development work.*

### Neo4j Operations
```bash
# Set dataset environment variable (defaults to "default" if not set)
export DATASET=${DATASET:-default}
export NEO_NAME="neo4j-${DATASET}"

# Launch dataset-specific container
./scripts/run-neo4j.sh ${DATASET}  # Or ./scripts/run-neo4j.sh bigdata, ./scripts/run-neo4j.sh clientA, etc.

# Quick connection test for development
docker exec -it ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3!

# Run schema validation
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/02-sanity.cypher

# Test vector search capability
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < queries/vector-search-verification.cypher
```

### ⚠️ **CRITICAL: cypher-shell Command Patterns**
```bash
# ✅ CORRECT: Single query via echo pipe
echo "MATCH (n) RETURN count(n);" | docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3!

# ✅ CORRECT: Script file input
docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! < script.cypher

# ✅ CORRECT: With parameters
echo "RETURN \$param;" | docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! --param "param => 'value'"

# ❌ WRONG: cypher-shell does NOT support -c flag
# docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! -c "MATCH (n) RETURN count(n);"
```

### Development Validation
```bash
# Test GraphRAG queries after environment setup
source venv/bin/activate && python scripts/08-graphrag-demo.py

# Run comprehensive business requirements test
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

### Debugging Commands
```bash
# Check container status
docker ps | grep ${NEO_NAME}

# View Neo4j logs for troubleshooting
docker logs ${NEO_NAME}

# Container restart (data loss - use for fresh start only)
docker stop ${NEO_NAME} && docker rm ${NEO_NAME}
```

### Complete Setup Validation
```bash
# Comprehensive setup verification
python scripts/07-validate-setup.py

# Expected output: ✅ All checks passed! Setup is complete.
```

### Clean Setup Sequence (Proven Working)
```bash
# 1. Start container
./scripts/run-neo4j.sh default

# 2. Create schema (constraints + indexes)  
scripts/01-create-schema.sh

# 3. Import data  
python scripts/02-import-sessions.py --dataset ${DATASET}
python scripts/03-decode-sms-content.py              # NEW: Extract SMS from base64
python scripts/04-import-additional-content.py       # NEW: Import all content types
python scripts/05-import-transcripts.py --dataset ${DATASET}

# 4. Generate embeddings
export OPENAI_API_KEY="sk-..."
./scripts/06-generate-embeddings.sh

# 5. Validate complete setup (only run after steps 1-4 complete)
python scripts/07-validate-setup.py

### Before Committing Changes
```bash
# Update dashboard and documentation counts
python scripts/update_counts.py

# Ensures consistent dashboard and documentation before commits
```

### Database Backup (ALWAYS use neo4j-admin dump)
```bash
# Create timestamped database dump
./scripts/backup-neo4j.sh ${DATASET}

# Creates: data/${DATASET}/neo4j-database-YYYY-MM-DD_HHMMSS.dump
# Note: Container stops briefly during dump (Community Edition requirement)

# To restore a dump:
docker stop neo4j-${DATASET}
docker run --rm \
  --volumes-from neo4j-${DATASET} \
  -v $(pwd)/data/${DATASET}/neo4j-database-YYYY-MM-DD_HHMMSS.dump:/dump.file \
  neo4j:5.26.7-community \
  neo4j-admin database load neo4j --from-stdin --overwrite-destination < /dump.file
docker start neo4j-${DATASET}
```

### Evaluation System Commands
```bash
# Interactive evaluation development (the "dance" approach)
PYTHONPATH=. python scripts/neo4j_query_executor.py eval EVAL-27

# Batch confidence processing for auto-promotion
PYTHONPATH=. python scripts/neo4j_query_executor.py confidence --batch

# Update progress dashboard
python scripts/evaluation_harness.py dashboard

# Run comprehensive validation suite
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < scripts/validation-suite.cypher

# Test graph visualization examples
docker exec -i ${NEO_NAME} cypher-shell -u neo4j -p Sup3rSecur3! < queries/graph-visualization-examples.cypher
```

### Test Documentation Update Sequence
```bash
# ⚠️ CRITICAL: Run after ANY test changes (add/remove/move tests)
# 1. Update all documentation counts
python scripts/update_counts.py

# 2. Regenerate performance histogram for GitHub Pages
pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only --benchmark-histogram=docs/benchmark-histogram

# 3. Regenerate HTML test results for GitHub Pages  
pytest tests/test_eval_queries.py::test_eval_functional \
    --html=docs/test-results.html --self-contained-html
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

#### Project Documentation
- [Data Mapping Guide](docs/data-mapping-guide.md) - **IMPORTANT**: Field naming conventions and data flow from source to Neo4j

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

## ⚠️ **CRITICAL: GitHub Workflow Rules**

### Branch Naming Convention (ENFORCED BY GITGUARD)
- **Pattern**: `^(feat|fix|docs|chore)/[0-9]+-[description]`
- **Rule**: Branch number MUST reference an existing GitHub issue
- **Examples**: 
  - ✅ `fix/27-post-merge-cleanup` (Issue #27 exists)
  - ❌ `fix/28-new-feature` (if Issue #28 doesn't exist)

### Issue-Branch-PR Workflow
1. **MUST verify**: Does the issue exist before creating branch?
2. **Continuation work**: Use original issue number (e.g., `fix/27-cleanup` for Issue #27 follow-up)
3. **New features**: Create issue first, then branch with same number
4. **NEVER assume**: Don't use "next number" without verifying issue exists

### Before Creating Any Branch:
```bash
# Check if issue exists first
gh issue view 28  # Verify issue exists before creating fix/28-*
```

**GitGuard Failure = Stop and Fix**: Never bypass security checks, always fix the root cause.

## Important Instructions
- **NEVER sign commits or changes as Claude/AI** - use standard git authorship only
- NEVER use emojis in any files or documentation unless explicitly requested by the User
- Only create documentation files when explicitly requested
- Always prefer editing existing files to creating new ones
- NEVER write Cypher queries into files without first validating them using the MCP Neo4j server
- ALWAYS test Cypher queries with MCP Neo4j server before documenting them

## ⚠️ Critical Terminology for Client Communication
- **"Failed" tests ≠ broken queries** - they are unprocessed tests awaiting confidence assessment
- **96.4% of "failed" tests work correctly** when properly evaluated (validated 2025-07-03)
- Use clear language: "needs assessment" not "failed" when discussing with clients
- The evaluation system has high reliability - most issues are process/assessment related, not technical failures

## Lessons Learned: Police Dataset Import

**Critical discoveries from analyzing law enforcement NDJSON data:**

1. **SMS Content Location**: SMS messages may be stored as base64-encoded XML in `Session.previewcontent` field, not in Content nodes. Always check all session fields before concluding data is missing.

2. **Content Extraction Patterns**:
   - **Intel Report & Social Network**: Extract from `fulltext[]` array
   - **Telephony & Generic File**: Extract from `documents[].text`
   - **Messaging (SMS)**: Decode from base64 `previewcontent`
   - **Entity Report**: Check both `documents[]` and `fulltext[]`

3. **Phone Object Scope**: Phone nodes handle BOTH telephony (calls) AND messaging (SMS) sessions. This is by design - phones are communication endpoints regardless of channel.

4. **Import Sequence Matters**:
   ```
   1. Base sessions (establishes relationships)
   2. SMS decode (extracts hidden content)
   3. Additional content (police reports, social media)
   4. Transcripts (external enrichment)
   5. Embeddings (enables semantic search)
   ```

5. **Content Discovery Strategy**:
   - First: Check what sessiontypes exist in data
   - Second: Examine sample sessions of each type
   - Third: Look for content in ALL fields (fulltext[], documents[], previewcontent)
   - Fourth: Test extraction methods before concluding data is missing

6. **Validation is Critical**: After each import step, validate:
   - Count of new nodes created
   - Content quality (sample checks)
   - Relationship integrity
   - Search capabilities (substring and semantic)

## Defensive Programming Requirements
**MANDATORY validation for EVERY code change**:

1. **Before editing**: Search for ALL occurrences (use `rg`, not grep/find)
2. **After editing**: Test what you modified (run scripts, execute queries, etc.)
3. **Before committing**: Verify all changes work and nothing broke
4. **Always report**: Tell user exactly what you validated

**NEVER claim success without proving it**
