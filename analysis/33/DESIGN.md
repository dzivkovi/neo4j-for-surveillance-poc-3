# Script Consolidation & Sprawl Elimination

## Problem / Metric
The project currently suffers from **scripts sprawl** across multiple directories and inconsistent implementations:
- 6+ duplicate embedding generation scripts with conflicting configurations (384 vs 1536 dimensions)
- 2 nearly identical validation scripts (`05-validate-setup.py` vs `verify-setup.py`)
- Scripts scattered across root folder (`*.sh`) and `scripts/*` subfolders  
- Missing operational scripts hidden from developers ("not in your face")
- Duplicated functionality between Python, Cypher, and shell implementations
- Inconsistent naming conventions and documentation patterns

**Measurable Impact**: 25+ script files across 4 different locations, causing confusion about which version is authoritative.

## Goal
Consolidate ALL operational scripts into a single flat `scripts/` directory, eliminating duplicates and establishing the "working" version of each capability. Follow "less is more" philosophy - every script should be immediately discoverable and obviously correct.

## Scope (M/S/W)

- [M] Consolidate all `.sh`, `.py`, `.cypher` scripts into flat `scripts/` directory
- [M] Remove duplicate/incompatible embedding generation scripts  
- [M] Establish single source of truth for each operational capability
- [M] Update all documentation references to new script locations
- [S] Standardize script naming conventions across languages
- [S] Add execution validation tests for critical scripts
- [W] Rewrite existing scripts in different languages (keep proven working versions)
- [W] Create new script capabilities beyond consolidation

## Acceptance Criteria
| # | Given | When | Then |
|---|-------|------|------|
| 1 | Developer needs to generate embeddings | They check scripts/ directory | Only one authoritative embedding script exists with clear usage docs |
| 2 | All scripts scattered across repo | After consolidation | All operational scripts live under scripts/ with no duplicates in root |
| 3 | Documentation references old paths | After path updates | All README.md and CLAUDE.md references point to new unified locations |
| 4 | Scripts with conflicting configs exist | After cleanup | Only verified working configurations remain (1536 dims, correct APIs) |
| 5 | Developer runs setup sequence | Using consolidated scripts | All scripts execute successfully from single location |
| 6 | Similar duplicate patterns exist | During flat structure migration | Implementer documents any additional duplicates discovered for future cleanup |

## Technical Design

### Current State Analysis
**Root Directory Scripts:**
- `04-generate-embeddings.sh` ✅ RENAMED IN PR #35 (was generate-embeddings.sh)
- `run_neo4j.sh` - Container management script

**Scripts Directory Structure:**
```
scripts/
├── cypher/
│   ├── 04-generate-embeddings.cypher ✅ RENAMED IN PR #35 (was 03-generate-embeddings.cypher)
│   └── [other cypher files]
├── python/
│   ├── 02-embed-text.py ❌ WRONG DIMENSIONS (384)
│   ├── 02-embed-text-openai.py ❌ LEGACY
│   └── [other python files]
└── 01-create-schema.sh ✅ WORKING
```

**Documentation with outdated references (found via grep):**
- `README.md` - references old `generate-embeddings.sh`
- `docs/embedding-generation-guide.md` - references old script name
- `docs/complete-setup-guide.md` - references old script name
- `docs/issue-26-context.md` - multiple references to old script names

### Target Architecture
**Single Flat Scripts Directory:**
```
scripts/
├── 01-create-schema.sh (moved from scripts/01-create-schema.sh)
├── 02-import-sessions.py (moved from scripts/python/02-import-sessions.py)
├── 03-import-transcripts.py (moved from scripts/python/03-import-transcripts.py)
├── 04-generate-embeddings.sh (already in root from PR #35)
├── 04-generate-embeddings.cypher (moved from scripts/cypher/)
├── 05-validate-setup.py (moved from scripts/python/05-validate-setup.py)
├── run-neo4j.sh (moved from root)
├── validation-suite.cypher (moved from scripts/cypher/)
├── neo4j-query-executor.py (moved from scripts/python/)
├── evaluation-harness.py (moved from scripts/python/)
├── graphrag-demo.py (moved from scripts/python/)
├── update-counts.py (moved from scripts/python/)
├── export-schema.sh (moved from scripts/)
└── [other operational scripts - all flat, no subfolders]
```

**Exception**: `queries/` folder remains separate (business-centric queries, not operational scripts)

## Implementation Steps

1. **Move all operational scripts to flat scripts/ directory**
   ```bash
   # Move root scripts
   mv run_neo4j.sh scripts/
   # Note: 04-generate-embeddings.sh already renamed in PR #35
   
   # Move from scripts/python/ to scripts/ (flat)
   mv scripts/python/02-import-sessions.py scripts/
   mv scripts/python/03-import-transcripts.py scripts/  
   mv scripts/python/05-validate-setup.py scripts/
   mv scripts/python/neo4j_query_executor.py scripts/
   mv scripts/python/evaluation_harness.py scripts/
   mv scripts/python/03-graphrag-demo.py scripts/graphrag-demo.py
   mv scripts/python/update_counts.py scripts/
   
   # Move from scripts/cypher/ to scripts/ (flat)  
   # Note: 04-generate-embeddings.cypher already renamed in PR #35
   mv scripts/cypher/04-generate-embeddings.cypher scripts/
   mv scripts/cypher/validation-suite.cypher scripts/
   mv scripts/cypher/02-sanity.cypher scripts/
   ```

2. **Flatten remaining operational scripts**
   - Move scripts/01-create-schema.sh to scripts/ (already there)
   - Move scripts/export-schema.sh to scripts/ (already there)
   - Keep queries/ folder separate (business queries, not operational)

3. **Remove duplicate/incompatible files**
   ```bash
   # Embedding generation duplicates
   rm scripts/python/02-embed-text.py  # Wrong dimensions (384 vs 1536)
   rm scripts/python/02-embed-text-openai.py  # Legacy version
   
   # Validation script duplicates  
   rm scripts/python/verify-setup.py  # Keep 05-validate-setup.py (more complete)
   # NOTE: validation-suite.cypher serves different purpose (business validation), keep it
   
   # Remove now-empty subdirectories after moves
   rmdir scripts/python scripts/cypher  # Only if empty after moves
   ```

4. **Update all path references**
   - Update `CLAUDE.md` command examples to use flat scripts/ paths
   - Update `README.md` references from scripts/python/ → scripts/
   - Update any scripts that call other scripts (relative paths)
   - Verify container volume mounts work with flat structure
   - Fix outdated references from PR #35 script renaming:
     - `README.md`: generate-embeddings.sh → 04-generate-embeddings.sh
     - `docs/embedding-generation-guide.md`: generate-embeddings.sh → 04-generate-embeddings.sh
     - `docs/complete-setup-guide.md`: generate-embeddings.sh → 04-generate-embeddings.sh
     - `docs/issue-26-context.md`: update all old script references

5. **Update script headers and documentation**
   - Ensure each script has clear usage comments
   - Update relative path references within scripts
   - Add standardized header format

6. **Validate consolidated setup**
   - Test complete setup sequence using new paths
   - Verify all command examples in documentation work
   - Run validation suite to ensure no regressions

## Testing Strategy

### Pre-Migration Validation
```bash
# Document current working state
docker exec -i $NEO_NAME cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/validation-suite.cypher
python scripts/python/05-validate-setup.py
```

### Post-Migration Validation  
```bash
# Test consolidated scripts
./scripts/run-neo4j.sh default
./scripts/01-create-schema.sh
python scripts/02-import-sessions.py
python scripts/03-import-transcripts.py
./scripts/04-generate-embeddings.sh
python scripts/05-validate-setup.py
```

### Documentation Validation
- Verify all command examples in `CLAUDE.md` execute successfully
- Test that new developer onboarding follows single script location
- Confirm no broken references to old script paths

## Risks & Considerations

**Migration Risks:**
- Scripts may have hidden dependencies on current file locations
- Container volume mounts might expect scripts in specific paths
- Git history for moved files becomes harder to track

**Mitigation Strategies:**
- Perform migration on feature branch for easy rollback
- Test each moved script individually before removing originals  
- Update docker commands to use new paths gradually
- Keep detailed commit messages documenting file moves

**Backward Compatibility:**
- Consider symlinks for critical scripts during transition period
- Update any CI/CD workflows that reference old script paths
- Document breaking changes for external users

**Dependencies:**
- No external dependencies require scripts in specific locations
- Container mounting can be updated to new paths
- MCP configuration uses container-internal paths (no changes needed)
