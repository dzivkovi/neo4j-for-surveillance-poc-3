# 06-ISSUE-26-CONTEXT.md - COMPLETE CONTEXT FOR DATASET-SPECIFIC CONTAINERS

**CRITICAL**: This document contains EVERYTHING needed to continue issue #26 work. Read this FIRST before any further development.

## ISSUE #26 OVERVIEW
**Goal**: Dataset-specific Neo4j containers with $NEO_NAME variable for < 10 second switching between investigations
**Status**: Phase 2 complete, moving to Phase 3 (multi-case support)

## WHAT WE ACCOMPLISHED (Phase 1 & 2)

### 1. CORE $NEO_NAME IMPLEMENTATION
- Created `run_neo4j.sh` - manages dataset-specific containers
- Updated ALL documentation to use $NEO_NAME variable instead of hardcoded "neo4j-sessions"
- Added comprehensive tests in `tests/test_dataset_containers.py`
- **VALIDATED**: Container switching works in < 10 seconds

### 2. ARCHAEOLOGICAL DISCOVERY - CONSTRAINTS/INDEXES MYSTERY SOLVED
**THE PROBLEM**: Original neo4j-sessions had 5 constraints that were missing in neo4j-default

**THE DISCOVERY**: 
- Constraints WERE added to `scripts/cypher/01-schema.cypher` as part of issue #7 (June 23-25, 2025)
- Design document at `analysis/7/DESIGN.md` shows the implementation plan
- BUT: Property names in schema were CORRECT for current data, different from original export

**KEY PROPERTY NAME DIFFERENCES**:
```
Schema (CORRECT):          Original Export (OUTDATED):
s.sessionguid         vs   s.session_guid
p.number             vs   p.phone_number  
e.email              vs   e.email_address
d.imei               vs   d.device_id
```

**ROOT CAUSE**: neo4j-sessions was manually modified after import, creating property name mismatches

### 3. COMPREHENSIVE TOOLS CREATED

#### A. Embedding Generation (Neo4j GenAI)
- **generate-embeddings.sh**: Wrapper script with proper API key handling
- **scripts/cypher/03-generate-embeddings.cypher**: Core Neo4j GenAI batch processing
- **VALIDATED**: Generates 1536-dim OpenAI embeddings for all Content nodes
- **USAGE**: `export OPENAI_API_KEY="sk-..." && ./generate-embeddings.sh`

#### B. Schema Management
- **scripts/cypher/05-validate-and-fix-schema.cypher**: Complete schema validation/fix
- **scripts/python/verify-setup.py**: Automated setup verification
- **CRITICAL**: These ensure ALL constraints and indexes are created properly

#### C. Database Analysis Tools  
- **scripts/python/export-neo4j-state.py**: Comprehensive JSON export
- **scripts/python/compare-neo4j-exports.py**: Container comparison
- **scripts/python/create-indexes.py**: Index creation with verification
- **scripts/export-schema.sh**: Human-readable schema export

#### D. Documentation
- **docs/complete-setup-guide.md**: Step-by-step setup from scratch
- **docs/embedding-generation-guide.md**: Embedding process documentation
- **Updated README.md**: Complete quick start process

## FINAL CLEAN SETUP PROCESS (VALIDATED)

```bash
# 1. Start container
./run_neo4j.sh default

# 2. Create complete schema (constraints + indexes)
./01-create-schema.sh

# 3. Import data
python scripts/python/02-import-sessions.py
python scripts/python/03-import-transcripts.py

# 4. Generate embeddings
export OPENAI_API_KEY="sk-..."
./generate-embeddings.sh

# 5. Validate complete setup
python scripts/python/05-validate-setup.py
```

**Key Improvements:**
- ✅ **Single schema creation script** that works reliably
- ✅ **Sequential numbered scripts** (01, 02, 03, 04, 05)
- ✅ **Individual command execution** for reliable constraint/index creation
- ✅ **Proven working sequence** tested by complete database wipe and rebuild

## EXPECTED FINAL STATE (VALIDATED)

### Constraints (5 total)
- `session_guid` on Session.sessionguid
- `phone_number` on Phone.number  
- `email_addr` on Email.email
- `device_imei` on Device.imei
- `alias_raw_unique` on Alias.rawValue

### Indexes (8+ additional)
- **Full-text**: ContentFullText, AliasText
- **Vector**: ContentVectorIndex (1536 dimensions, COSINE similarity)
- **Spatial**: locationGeo (POINT type)
- **Range**: sessionDuration, session_createddate, session_sessiontype, person_name_index
- **Automatic**: LOOKUP indexes + backing indexes for constraints

### Node Counts (Typical)
- Session: 265, Content: 215+ (with embeddings), Person: 40, Phone: 24, Email: 18, Device: 17, Location: 41, Alias: 89+

### Embeddings
- ALL Content nodes with text have 1536-dimensional OpenAI embeddings
- Generated using Neo4j GenAI batch API: `genai.vector.encodeBatch()`

## PHASE 3 - NEXT WORK (Multi-Case Support)

### WHAT'S NEEDED:
1. **Data Structure**: Create data/whiskey/, data/gantry/ folders
2. **Import Scripts**: Add --case parameter to import scripts  
3. **Container Management**: Enhance run_neo4j.sh for case-based containers
4. **Documentation**: Update for multi-case workflow

### APPROACH:
- Build on existing $NEO_NAME infrastructure
- Use case names as container suffixes: neo4j-whiskey-jack, neo4j-gantry
- Maintain same schema/setup process for each case

## CRITICAL TECHNICAL DETAILS

### Neo4j GenAI Embedding Parameters
```cypher
CALL genai.vector.encodeBatch(texts, 'OpenAI', {
    token: $openai_api_key,
    model: 'text-embedding-3-small',
    dimensions: 1536
}) YIELD index, vector
```

### Container Environment Variables
```bash
NEO_NAME="neo4j-${DATASET}"    # Where DATASET can be: default, whiskey-jack, gantry, etc.
NEO4J_PLUGINS='["genai"]'      # Required for embedding generation
```

### Critical Files Modified
- `README.md`: Added embedding generation step
- `CLAUDE.md`: Updated essential commands to use $NEO_NAME
- `run_neo4j.sh`: Core container management
- `tests/test_dataset_containers.py`: Validation tests

## VALIDATION COMMANDS

```bash
# Check setup is complete
python scripts/python/verify-setup.py

# Should show: ✅ All checks passed! Setup is complete.

# Quick manual verification
docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! -c "SHOW CONSTRAINTS; SHOW INDEXES;"
```

## TROUBLESHOOTING KNOWLEDGE

### Common Issues:
1. **Constraints not created**: Run 05-validate-and-fix-schema.cypher
2. **Wrong property names**: Schema is correct, exports may show outdated names
3. **Embeddings missing**: Check OPENAI_API_KEY and GenAI plugin enabled
4. **Silent failures**: Always run verify-setup.py after setup

### File Dependencies:
- `01-schema.cypher` → `05-validate-and-fix-schema.cypher` → `verify-setup.py`
- All import scripts depend on container being started with GenAI plugin
- Embedding generation requires API key and Content nodes with text

## GIT BRANCH STATUS
- Branch: `feat/26-dataset-specific-containers`
- Commits: Basic implementation + comprehensive tools
- Ready for: Multi-case support implementation

## BREADCRUMB TRAIL
- `analysis/7/DESIGN.md`: Original constraints implementation plan
- `data/sessions/neo4j-export-20250706_005625.json`: Original container export
- Issue #7: Where constraints were added (June 23-25, 2025)
- `analysis/2025-01-06/`: All discovery documents (in .gitignore)

---

**NEXT SESSION INSTRUCTIONS**:
1. Read this document FIRST
2. Run `python scripts/python/verify-setup.py` to confirm current state
3. Continue with Phase 3: Multi-case support
4. All tools are ready and validated - build on this foundation