---
description: Develop Cypher query for evaluation test
arguments: test_number
---

# Interactive Evaluation Test Development

Opens EVAL-NN test file and guides interactive query development using Neo4j MCP tools.

## Usage

```
/eval 05
/eval EVAL-42
```

## Workflow

This command follows the proven "dance" methodology for interactive query development:

1. **Find Test File**: Search `evals/*/EVAL-NN.md` across all folders
2. **Load Business Context**: Parse evaluation_tests.md table for business requirements
3. **Interactive Development**: Use Neo4j MCP tools to develop and test queries
4. **Query Recording**: Replace placeholder with working Cypher query
5. **Manual Steps Required**: 
   - Execute query and record actual results
   - Add confidence assessment section (see template below)
   - Update validation status to PASSED
6. **Auto-Promotion**: Run the confidence command to auto-promote if ≥80% confidence

## Next Steps After Query Development

After `/eval NN` completes, you need to:

1. **Add confidence section** to the test file (replace NN with your test number):
```markdown
## Confidence Assessment

**Query Results**: [describe what you found]
**Business Question**: "[copy from Expected Answer]"
**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED
```

2. **Run auto-promotion** (replace NN with your test number):
```bash
PYTHONPATH=. python scripts/python/neo4j_query_executor.py confidence --test-id EVAL-NN
```

**Example**:
```bash
PYTHONPATH=. python scripts/python/neo4j_query_executor.py confidence --test-id EVAL-09
```

## Confidence Scoring

- **Y** (Correct) = 80% confidence → Auto-promote to PASSED
- **Partial** (Partially correct) = 70% confidence → Stay in REVIEW  
- **N** (Incorrect) = 30% confidence → Auto-fail to FAILED

## Error Handling

- **Multiple files found**: Abort with error message
- **Invalid test ID**: Show valid range (01-77)
- **Missing test file**: Suggest creating new test
- **MCP connection errors**: Abort and ask human operator to check Neo4j connection

## Important: Always End Commands With Next Steps

After completing query development, ALWAYS print the next steps template and commands for the user:

```
✅ Query development complete! Next steps:

1. Add this confidence section to your test file:
## Confidence Assessment

**Query Results**: [describe what you found]
**Business Question**: "[copy from Expected Answer]"
**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED

2. Run auto-promotion (replace NN with your test number):
PYTHONPATH=. python scripts/python/neo4j_query_executor.py confidence --test-id EVAL-NN

3. Verify the test moved to evals/passed/
```

## Integration

Works with existing evaluation harness system:
- Reads current test files from 5-folder structure
- Updates files in place with new query and confidence sections
- Compatible with automated confidence processor for batch operations