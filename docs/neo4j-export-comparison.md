# Neo4j Export and Comparison Tools

Tools for exporting and comparing Neo4j database states across different containers to ensure consistency.

## Quick Reference

```bash
# Export from any container
export CASE_NAME=sessions  # or default, whiskey, etc.
./scripts/export-schema.sh ${CASE_NAME}
python scripts/python/export-neo4j-state.py --case ${CASE_NAME}

# Compare any two exports
python scripts/python/compare-neo4j-exports.py \
    data/case1/neo4j-export-*.json \
    data/case2/neo4j-export-*.json
```

## Available Tools

### 1. Text Export (`scripts/export-schema.sh`)
Quick human-readable export for manual inspection.

**Output**: `data/{case}/schema-export-{timestamp}.txt`

**Contains**: Labels, relationships, counts, indexes, constraints, sample data

### 2. JSON Export (`scripts/python/export-neo4j-state.py`)
Comprehensive export for automated comparison.

**Output**: `data/{case}/neo4j-export-{timestamp}.json`

**Contains**: Complete schema, all properties, statistics, sample data (5 nodes per label)

### 3. Comparison Tool (`scripts/python/compare-neo4j-exports.py`)
Automated diff between two JSON exports showing:
- Schema differences (labels, relationships)
- Count differences with +/- indicators
- Property differences per label
- Index/constraint differences

## Usage Example

```bash
# 1. Export from original container
docker start neo4j-sessions
python scripts/python/export-neo4j-state.py --case sessions

# 2. Export from new container
./run_neo4j.sh default
# After loading data...
python scripts/python/export-neo4j-state.py --case default

# 3. Compare results
python scripts/python/compare-neo4j-exports.py \
    data/sessions/neo4j-export-*.json \
    data/default/neo4j-export-*.json
```

## What to Check

1. **Schema Consistency**: Missing labels, relationships, or properties
2. **Data Integrity**: Different counts or missing data types  
3. **Index Coverage**: All required indexes present
4. **No Duplicates**: Clean import without redundant nodes

## Directory Structure

```
data/
├── default/
│   ├── neo4j-export-{timestamp}.json
│   └── schema-export-{timestamp}.txt
├── sessions/
│   └── ...exports...
└── whiskey/
    └── ...exports...
```

## Best Practices

- Always export BEFORE making changes (baseline)
- Keep exports to track schema evolution
- Use JSON export for detailed comparison
- Use text export for quick manual review