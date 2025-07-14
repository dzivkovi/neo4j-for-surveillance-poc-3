# EVAL Query Test Suite

Automated testing framework for Neo4j POLE POC evaluation queries.

## Quick Start

```bash
# Install dependencies
pip install -r requirements-test.txt

# Run all tests
pytest tests/test_eval_queries.py -v

# Run specific test
pytest tests/test_eval_queries.py::test_eval_functional[EVAL-02] -v

# Generate web-ready reports
export DATASET=bigdata
pytest tests/test_eval_queries.py::test_eval_functional \
    --html=docs/test-results.html --self-contained-html

pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only --benchmark-histogram=docs/benchmark-histogram

# Skip slow tests
pytest tests/test_eval_queries.py -v -m "not slow"
```

## Environment Variables

- `NEO4J_URI`: Neo4j connection (default: bolt://localhost:7687)
- `NEO4J_USER`: Username (default: neo4j)
- `NEO4J_PASSWORD`: Password (default: Sup3rSecur3!)
- `NEO4J_DATABASE`: Database name (default: neo4j)

## Performance Analysis

```bash
# Compare two benchmark runs
pytest-benchmark compare benchmark1.json benchmark2.json

# Generate HTML report
pytest tests/test_eval_queries.py --benchmark-only --benchmark-autosave
pytest-benchmark compare --html=report.html
```

## Adding New Tests

Simply add new `EVAL-NN.md` files to `evals/passed/`. They will be discovered automatically.

## Evaluation-Driven Development Workflow

This project uses a unique **evaluation-driven development workflow** that combines business requirements validation with automated performance testing:

### The Complete Loop

```bash
# Single command handles the entire workflow
python scripts/update_counts.py
```

**What happens:**
1. **Benchmark Execution**: Runs pytest performance tests against all passed evaluations
2. **Source File Updates**: Updates individual `evals/*/EVAL-*.md` files with real timestamps and performance data
3. **Dashboard Generation**: Reads from EVAL files to generate consistent `evals/README.md` dashboard
4. **Documentation Sync**: Updates all count references across documentation

### Business Value

This workflow provides **traceability from business requirements to performance metrics**:

- ✅ **Requirements**: Each EVAL-XX corresponds to real law enforcement scenarios
- ✅ **Implementation**: Cypher queries that solve the business problems  
- ✅ **Validation**: Automated tests verify queries work correctly
- ✅ **Performance**: Benchmarks ensure queries meet <5s response requirements
- ✅ **Reporting**: Dashboard shows stakeholders exactly what's validated and how fast

### Key Benefits

- **Single Source of Truth**: EVAL files contain authoritative timestamps and performance data
- **No Data Inconsistencies**: Dashboard always reflects what's actually in the files
- **Business-Technical Bridge**: Links evaluation scenarios directly to performance metrics
- **Client Confidence**: Shows exactly which surveillance scenarios are validated and tested

### For GitHub Pages Demo

After workflow updates, regenerate public-facing reports:

```bash
# Regenerate performance histogram for GitHub Pages
pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only --benchmark-histogram=docs/benchmark-histogram

# Regenerate HTML test results for GitHub Pages
pytest tests/test_eval_queries.py::test_eval_functional \
    --html=docs/test-results.html --self-contained-html
```

**⚠️ Important**: Both the SVG file (`docs/benchmark-histogram-eval-queries.svg`) and HTML report (`docs/test-results.html`) must be regenerated after test changes or they will show outdated data on the GitHub Pages demo site.