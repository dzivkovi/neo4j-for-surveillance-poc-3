# Pytest HTML Reports Guide

All test reports are stored in `docs/` for easy access and web publishing.

## Files Generated

1. **test-results.html** - Comprehensive test results with pass/fail visualization
2. **benchmark-histogram-eval-queries.svg** - Performance histogram visualization
3. **.benchmarks/Linux-CPython-3.12-64bit/*.json** - Raw benchmark data for comparisons

## Viewing the Reports

### 1. Test Results HTML Report

Open in your browser:
```bash
# On Linux/WSL
xdg-open docs/test-results.html

# On macOS
open docs/test-results.html

# Or simply copy the path and open in browser
echo "file://$PWD/docs/test-results.html"

# Or view live on GitHub Pages
echo "https://dzivkovi.github.io/neo4j-for-surveillance-poc-3/test-results.html"
```

**Features:**
- Interactive pass/fail summary with pie chart
- Expandable test details
- Error messages and stack traces for failures
- Test duration for each test
- Environment details (Python version, plugins, etc.)
- Filtering by outcome (passed/failed/skipped)
- Search functionality

### 2. Benchmark Histogram

View the SVG file:
```bash
# Open in default image viewer
xdg-open docs/benchmark-histogram-eval-queries.svg

# Or in browser
echo "file://$PWD/docs/benchmark-histogram-eval-queries.svg"

# Or view live on GitHub Pages
echo "https://dzivkovi.github.io/neo4j-for-surveillance-poc-3/benchmark-histogram-eval-queries.svg"
```

**Shows:**
- Performance distribution across all queries
- Min/max/mean execution times
- Visual comparison of query performance

## Quick Start

Generate fresh reports:
```bash
# Set correct environment
export DATASET=bigdata

# Generate test report and benchmark histogram (web-ready)
pytest tests/test_eval_queries.py::test_eval_functional \
    --html=docs/test-results.html --self-contained-html

pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only --benchmark-histogram=docs/benchmark-histogram
```

## Generating Different Report Types

### Basic Test Report
```bash
pytest tests/test_eval_queries.py --html=report.html --self-contained-html
```

### With Custom CSS (prettier)
```bash
pytest tests/test_eval_queries.py --html=report.html --css=custom.css
```

### JSON Report (for CI/CD integration)
```bash
pytest tests/test_eval_queries.py --json-report --json-report-file=report.json
```

### Benchmark Reports

#### Generate benchmark with statistics
```bash
pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only \
    --benchmark-columns=min,max,mean,stddev,median,iqr,outliers,rounds \
    --benchmark-sort=mean
```

#### Save benchmark data for comparison
```bash
# Run 1
pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only \
    --benchmark-json=benchmark-1.json

# Run 2 (after changes)
pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only \
    --benchmark-json=benchmark-2.json

# Compare
pytest-benchmark compare benchmark-1.json benchmark-2.json
```

#### Export to CSV
```bash
pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only \
    --benchmark-json=benchmark.json

# Then convert
pytest-benchmark compare benchmark.json --csv=results.csv
```

## Advanced Features

### 1. Filtering Tests in Report
```bash
# Only failed tests
pytest tests/test_eval_queries.py --html=failures.html --self-contained-html -x

# By marker
pytest tests/test_eval_queries.py -m "not slow" --html=fast-tests.html
```

### 2. Adding Screenshots/Extra Content
```python
# In your test
def test_example(extra):
    extra.append(extras.text("Custom text"))
    extra.append(extras.url("https://example.com"))
    extra.append(extras.image("screenshot.png"))
```

### 3. Performance Thresholds
```bash
# Fail if any test takes >2 seconds
pytest tests/test_eval_queries.py --benchmark-only \
    --benchmark-max-time=2.0
```

### 4. Continuous Monitoring
```bash
# Save with timestamp
pytest tests/test_eval_queries.py::test_eval_performance \
    --benchmark-only \
    --benchmark-save=run-$(date +%Y%m%d-%H%M%S)

# List all saved benchmarks
pytest-benchmark list

# Compare last two
pytest-benchmark compare
```

## Tips

1. **For CI/CD**: Use `--json-report` for machine-readable output
2. **For debugging**: Use `--html` with `--tb=short` for concise tracebacks
3. **For performance tracking**: Use `--benchmark-autosave` to automatically save results
4. **For presentations**: Use `--benchmark-histogram` for visual performance graphs

## Example Dashboard Script

Create a simple dashboard:
```bash
#!/bin/bash
# run-dashboard.sh

# Run tests
pytest tests/test_eval_queries.py \
    --html=dashboard.html \
    --self-contained-html \
    --benchmark-only \
    --benchmark-histogram=perf

# Open in browser
xdg-open dashboard.html
```