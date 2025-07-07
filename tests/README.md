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

## Keeping Documentation Updated

After adding/moving tests, update all count references:
```bash
python scripts/python/update_counts.py
```