# Surveillance Graph Analytics Project

End-to-end sandbox that ingests *sessions.ndjson* (law-enforcement communication sessions) into Neo4j 5.x, builds full-text & vector indexes, and runs evaluation queries defined by client.

[![Project Board](https://img.shields.io/badge/Project%20Board-Kanban-blue)](https://github.com/users/dzivkovi/projects/1)

## Quick Start

```bash
git clone https://github.com/your-org/surveillance-neo4j-analytics.git
cd surveillance-neo4j-analytics

# 1. spin-up docker container with Neo4j 5.x Community Edition with APOC and GDS
docker run --name neo4j-sessions \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/Sup3rSecur3! \
  -e NEO4J_PLUGINS='["apoc","graph-data-science"]' \
  -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*,db.* \
  -e NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.*,db.* \
  -d neo4j:5.26.7-community

# 2. create constraints, indexes & full-text/vector indexes
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/01-schema.cypher

# 3. build virtualenv and import data + embeddings
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r scripts/python/requirements.txt

python scripts/python/01-import-data.py         # ~2 min for 200 sessions
python scripts/python/02-embed-text.py          # adds 384-dim vectors

# 4. run sanity checks & evaluation queries
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/02-sanity.cypher
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < queries/eval-suite.cypher
```

GraphRAG Example (LangChain + Neo4j) lives in
`scripts/python/03-graphrag-demo.py` and shows how to answer “Does Fred
discuss travel plans?” using similarity search over the vector index.

## Operational Notes

### Docker Container Management

The Neo4j container requires specific configuration for vector search and procedures:

```bash
# Stop and remove current container (data will be lost)
docker stop neo4j-sessions && docker rm neo4j-sessions

# Start with proper configuration (matches CLAUDE.md specifications)
docker run --name neo4j-sessions \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/Sup3rSecur3! \
  -e NEO4J_PLUGINS='["apoc","graph-data-science"]' \
  -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*,db.* \
  -e NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.*,db.* \
  -d neo4j:5.26.7-community
```

### Data Restoration Workflow

After container restart, follow this sequence (consistent with CLAUDE.md):

```bash
# 1. Schema first (creates vector index)
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! -f scripts/cypher/01-schema.cypher

# 2. Import data (265 sessions in test dataset)
python scripts/python/01-import-data.py

# 3. Generate embeddings (384-dim vectors)
python scripts/python/02-embed-text.py

# 4. Verify import
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! -f scripts/cypher/02-sanity.cypher
```

## Business Requirements Validation

### Core Investigative Questions Answered

This system addresses real law enforcement needs by answering critical surveillance questions:

**Entity Relationships:**

- "Who are William Eagle's top associates?" → Richard Eagle (29 interactions), Fred Merlin (18), Kenzie Hawk (12)
- "How does Kenzie communicate with Owen?" → SMS (24 instances), Telephony (7 instances)  
- "What are Kenzie's IMEIs?" → Two devices with 83 and 1 sessions respectively

**Device Intelligence:**

- "Which IMEIs are associated with phone 9366351931?" → Multiple device associations revealing device sharing/transfers
- "Who has been using devices with IMEI 359847107165930?" → William Eagle (75 sessions), Ted Dowitcher (1 session)

**Content Investigation:**

- "Does Fred discuss travel plans?" → Yes, multiple instances from Feb 9-14, 2020 including Mobile→Miami→Port Miami meetings
- "Has Kenzie referenced a shed?" → Yes, equipment storage discussions with Mildred and Owen
- "Are there any references to sago palms?" → Yes, landscaping orders with suspicious timing patterns

**Operational Intelligence:**

- Time-based filtering: 44 morning sessions, pertinent classifications, audio content analysis
- Communication patterns: SMS vs telephony usage by individual
- Network analysis: Multi-hop relationship traversals revealing investigation targets

### Running the Evaluation Suite

Validate that your deployment meets all business requirements:

```bash
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! -f queries/eval-suite.cypher
```

This comprehensive test suite covers:

- **Schema validation** (constraints, indexes, vector search capability)
- **Core business queries** (entity relationships, device tracking, communication patterns)  
- **Content search** (full-text and semantic search for surveillance keywords)
- **Data quality** (completeness, integrity, performance)

Expected results include specific entity counts, relationship patterns, and content discoveries that prove the system's investigative value.

## MCP Integration (Natural Language Queries)

For eliminating Cypher learning curve, see `README_MCP.md` which demonstrates:

- Plain English database queries via Claude Desktop
- Automatic translation to optimized Cypher
- Zero syntax errors and conversational data exploration

## Query Collections

- `queries/eval-suite.cypher` - Comprehensive business requirements validation
- `queries/data-exploration.cypher` - 8 sections of validation queries
- `queries/vector-search-verification.cypher` - Vector similarity testing
- `queries/investigative.cypher` - Law enforcement use cases

## Development Workflow

### Business Rules Tracking

Project discoveries and implementation priorities are tracked in `docs/business-rules/`:

```bash
# View current business rules and priorities
cat docs/business-rules/README.md

# Update the index after adding/editing rules
bash scripts/bash/generate-business-rules-readme.sh > docs/business-rules/README.md
```

This system captures lessons learned from client meetings, technical analysis, and investigation findings to guide development priorities and ensure nothing important is forgotten.

## Design Decisions

- **Session-centric POLE** schema – direct 1-to-1 mapping of NDJSON fields → graph nodes, minimising cognitive overhead while still matching law-enforcement ontologies (POLE / CASE / UCO). Sources ([1](https://neo4j.com/blog/government/graph-technology-pole-position-law-enforcement/), [2](https://caseontology.org/ontology/start.html))
- **Immutable raw data** under `data` – keeps provenance clear and simplifies reproducibility ([3](https://neo4j.com/developer/data-import/), [4](https://neo4j.com/docs/operations-manual/current/backup-restore/))
- **Vector search** via Neo4j OSS 5.11+ `VECTOR INDEX` for semantic questions; embeddings generated with `sentence-transformers/all-MiniLM-L6-v2` (384 dims) ([5](https://github.com/neo4j/neo4j/releases/tag/5.11.0), [6](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/))
- **GraphRAG** demo uses Neo4j retriever from LangChain so analysts can prototype QA pipelines without extra infra ([7](https://neo4j.com/developer/genai-ecosystem/))

## For AI Assistants

See `CLAUDE.md` for project context and documentation links.
