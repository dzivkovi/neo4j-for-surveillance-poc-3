# Unified Test & Benchmark Framework for Neo4j POLE POC

## Problem / Metric

Currently, 50+ validated Cypher queries in `evals/passed/EVAL-NN.md` files require manual execution to verify correctness and measure performance. This creates:
- No automated regression detection when data/schema changes
- Manual performance testing taking hours per full run
- No standardized way to compare query performance across datasets
- Risk of queries breaking without detection

**Metric**: Reduce validation time from 2 hours to <3 minutes while capturing detailed performance metrics.

## Goal

Create a minimal, production-ready pytest framework that automatically discovers and tests all EVAL queries, verifies functional correctness, captures performance metrics, and runs unchanged against any Neo4j 5 instance.

## Scope (M/S/W)

- [M] Auto-discover all `evals/passed/EVAL-*.md` files
- [M] Extract Cypher queries using robust markdown parsing
- [M] Execute queries and verify they run without error
- [M] Capture server-side execution time (ms)
- [M] Support result validation against expected values
- [S] Benchmark performance with statistical analysis
- [S] Export performance data to JSON
- [S] Support fuzzy text matching for semantic results
- [W] Update markdown files with timing data
- [W] LLM-as-judge integration (future extensibility hook only)

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | 50+ EVAL files in evals/passed/ | Running pytest | All files are discovered and tested automatically |
| 2 | EVAL file with Cypher query | Test executes | Query runs and basic pass/fail is recorded |
| 3 | Query with expected count/score | Test runs | Validates actual vs expected within tolerance |
| 4 | Any query execution | Test completes | Server timing captured in milliseconds |
| 5 | New EVAL file added | No code changes | Test suite picks it up automatically |
| 6 | Remote Neo4j instance | NEO4J_URI env var set | Tests run against remote instance |
| 7 | Performance regression | Running benchmarks | JSON export shows timing changes |

## Technical Design

### Architecture

```text
tests/
├── conftest.py          # Neo4j fixtures + test generation
├── test_eval_queries.py # Main test functions  
└── eval_parser.py       # Markdown parsing (~100 lines)
```

### Key Components

1. **Parser**: Hybrid AST (mistune) + regex fallback for robustness
2. **Test Generator**: pytest_generate_tests with parametrization
3. **Validators**: Three-tier (basic/numeric/semantic) progressive validation
4. **Benchmarking**: Dual approach (server timing + pytest-benchmark)

### Data Model

```python
@dataclass
class EvalTestCase:
    id: str              # "EVAL-02"
    query: str           # Cypher query text
    expected: Dict       # Parsed expected results
    metadata: Dict       # Category, etc.
```

## Detailed Implementation

### 1. Create `tests/eval_parser.py` (COMPLETE CODE)

```python
"""
Parser for EVAL-NN.md files - extracts Cypher queries and expected results.
Supports both AST parsing (robust) and regex fallback for edge cases.
"""
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import re

# Try to use mistune for robust parsing, fallback to regex if not available
try:
    import mistune
    USE_AST = True
except ImportError:
    USE_AST = False


@dataclass
class EvalTestCase:
    """Represents a single test case from an EVAL file"""
    id: str                    # e.g., "EVAL-02"
    file_path: Path           # Full path to source file
    query: str                # Cypher query text
    expected_result: Dict     # Parsed expected values
    metadata: Dict            # Category, Duration-ms, etc.


def parse_eval_files(directory: Path) -> List[EvalTestCase]:
    """
    Parse all EVAL-NN.md files in directory and extract test cases.
    
    Args:
        directory: Path to evals/passed/ directory
        
    Returns:
        List of EvalTestCase objects ready for pytest
    """
    test_cases = []
    
    # Sort for consistent test ordering
    for file_path in sorted(directory.glob("EVAL-*.md")):
        try:
            case = extract_test_case(file_path)
            if case:
                test_cases.append(case)
        except Exception as e:
            # Log but don't fail - defensive programming
            print(f"Warning: Failed to parse {file_path}: {e}")
    
    return test_cases


def extract_test_case(file_path: Path) -> Optional[EvalTestCase]:
    """Extract single test case from EVAL file"""
    content = file_path.read_text(encoding='utf-8')
    
    # Extract components
    query = extract_cypher_query(content)
    if not query:
        return None
    
    expected = extract_expected_result(content)
    metadata = extract_metadata(content)
    
    return EvalTestCase(
        id=file_path.stem,
        file_path=file_path,
        query=query,
        expected_result=expected,
        metadata=metadata
    )


def extract_cypher_query(content: str) -> Optional[str]:
    """Extract Cypher query using AST or regex fallback"""
    if USE_AST:
        # Use mistune AST parsing (more robust)
        md = mistune.create_markdown(renderer='ast')
        ast = md(content)
        
        in_query_section = False
        for node in ast:
            # Check for ### Query heading
            if node.get('type') == 'heading' and node.get('level') == 3:
                heading_text = extract_text_from_ast(node)
                in_query_section = 'query' in heading_text.lower()
            
            # Extract cypher code block
            elif in_query_section and node.get('type') == 'code_block':
                if node.get('info', '').lower() == 'cypher':
                    return node.get('raw', '').strip()
    
    # Fallback to regex (handles edge cases)
    pattern = r'### Query\s*```cypher\s*(.*?)\s*```'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if match:
        query = match.group(1).strip()
        # Also check for inline expected values
        query = extract_inline_expected(query)
        return query
    
    return None


def extract_text_from_ast(node: dict) -> str:
    """Helper to extract text from AST node"""
    if node.get('type') == 'text':
        return node.get('raw', '')
    
    text_parts = []
    for child in node.get('children', []):
        if isinstance(child, dict):
            text_parts.append(extract_text_from_ast(child))
    
    return ' '.join(text_parts).strip()


def extract_inline_expected(query: str) -> str:
    """Extract and process inline -- expected: comments"""
    # Store expected values found in comments
    expected_pattern = r'--\s*expected:\s*(.+)$'
    matches = re.findall(expected_pattern, query, re.MULTILINE)
    
    if matches:
        # Store in global for later processing (hacky but works)
        global _inline_expected
        _inline_expected = matches[0].strip()
    
    # Return query without comments
    return re.sub(expected_pattern, '', query, flags=re.MULTILINE).strip()


def extract_expected_result(content: str) -> Dict:
    """
    Extract expected results from ### Actual Result section.
    Handles various formats found in EVAL files.
    """
    result = {}
    
    # Check for inline expected first
    if hasattr(extract_inline_expected, '_inline_expected'):
        inline = getattr(extract_inline_expected, '_inline_expected', None)
        if inline:
            result['inline'] = inline
            delattr(extract_inline_expected, '_inline_expected')
    
    # Pattern for ### Actual Result section
    pattern = r'### Actual Result\s*```\s*(.*?)\s*```'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return result
    
    result_text = match.group(1).strip()
    
    # Parse different result formats
    # Format 1: field_name: value
    for line in result_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Try to parse numeric values
            if value.replace('.', '', 1).replace('-', '', 1).isdigit():
                if '.' in value:
                    result[key] = float(value)
                else:
                    result[key] = int(value)
            else:
                result[key] = value
    
    # Common aliases for count fields
    count_fields = ['discussions_voyage', 'shed_sessions', 'travel_discussions', 
                   'session_count', 'count', 'total']
    score_fields = ['meilleur_score', 'relevance_score', 'max_score', 'score']
    
    # Normalize to standard keys
    for field in count_fields:
        if field in result:
            result['count'] = result[field]
            break
    
    for field in score_fields:
        if field in result:
            result['score'] = result[field]
            break
    
    return result


def extract_metadata(content: str) -> Dict:
    """Extract metadata from EVAL file header"""
    metadata = {}
    
    # Parse header metadata (first 20 lines)
    lines = content.split('\n')[:20]
    
    for line in lines:
        if line.startswith('Category:'):
            metadata['Category'] = line.split(':', 1)[1].strip()
        elif line.startswith('Duration-ms:'):
            value = line.split(':', 1)[1].strip()
            if value != '—' and value.isdigit():
                metadata['Duration-ms'] = int(value)
        elif line.startswith('Status:'):
            metadata['Status'] = line.split(':', 1)[1].strip()
        elif line.startswith('Added:'):
            metadata['Added'] = line.split(':', 1)[1].strip()
    
    return metadata


# Example usage for testing parser independently
if __name__ == "__main__":
    from pathlib import Path
    evals_dir = Path("evals/passed")
    cases = parse_eval_files(evals_dir)
    print(f"Found {len(cases)} test cases")
    for case in cases[:3]:
        print(f"\n{case.id}:")
        print(f"  Query: {case.query[:50]}...")
        print(f"  Expected: {case.expected_result}")
        print(f"  Category: {case.metadata.get('Category', 'Unknown')}")
```

### 2. Update `tests/conftest.py` (ADD THIS CODE)

```python
# Add these imports at the top
from pathlib import Path
from eval_parser import parse_eval_files

# Add this after existing fixtures
_TEST_CASES = None  # Cache for performance

def pytest_generate_tests(metafunc):
    """
    Dynamically generate test cases from EVAL files.
    This hook is called during test collection phase.
    """
    if "eval_case" in metafunc.fixturenames:
        global _TEST_CASES
        
        # Parse files only once
        if _TEST_CASES is None:
            eval_dir = Path(__file__).parent.parent / "evals" / "passed"
            _TEST_CASES = parse_eval_files(eval_dir)
            print(f"\nDiscovered {len(_TEST_CASES)} EVAL test cases")
        
        # Parametrize with descriptive IDs
        metafunc.parametrize(
            "eval_case",
            _TEST_CASES,
            ids=[case.id for case in _TEST_CASES]
        )
```

### 3. Create `tests/test_eval_queries.py` (COMPLETE CODE)

```python
"""
Test suite for EVAL queries - functional and performance testing.
Automatically runs all queries from evals/passed/EVAL-*.md files.
"""
import pytest
import time
from typing import Dict, List, Any
from rapidfuzz import fuzz


def test_eval_functional(eval_case, neo4j_session):
    """
    Test functional correctness of EVAL queries.
    
    This test:
    1. Executes the Cypher query
    2. Validates it completes without error
    3. Checks results against expected values (if present)
    4. Captures execution metrics
    """
    query = eval_case.query
    expected = eval_case.expected_result
    
    # Execute query and measure time
    start_time = time.perf_counter()
    
    try:
        result = neo4j_session.run(query)
        records = list(result)  # Consume all records
        summary = result.consume()
        
        # Capture metrics
        server_time_ms = summary.result_available_after
        driver_time_ms = (time.perf_counter() - start_time) * 1000
        
    except Exception as e:
        pytest.fail(f"Query execution failed for {eval_case.id}: {e}\nQuery: {query}")
    
    # Basic assertion - query executed
    assert summary is not None, "Query should complete successfully"
    assert server_time_ms is not None, "Server timing should be available"
    
    # Validate results if expected values present
    if expected:
        validate_results(records, expected, eval_case.id)
    
    # Log metrics for analysis
    print(f"\n{eval_case.id}: server={server_time_ms}ms, driver={driver_time_ms:.1f}ms, rows={len(records)}")


def validate_results(records: List[Any], expected: Dict, test_id: str):
    """
    Validate query results against expected values.
    Supports count validation, score validation, and text similarity.
    """
    # Count validation
    if 'count' in expected:
        actual_count = len(records)
        expected_count = expected['count']
        
        # Allow 10% tolerance for counts
        tolerance = max(1, int(expected_count * 0.1))
        assert abs(actual_count - expected_count) <= tolerance, \
            f"{test_id}: Expected {expected_count}±{tolerance} rows, got {actual_count}"
    
    # Score validation (if query returns scores)
    if 'score' in expected and records:
        # Extract numeric scores from results
        scores = extract_scores(records)
        if scores:
            max_score = max(scores)
            expected_score = float(expected['score'])
            
            # Allow 20% tolerance for scores
            tolerance = expected_score * 0.2
            assert abs(max_score - expected_score) <= tolerance, \
                f"{test_id}: Expected score {expected_score}±{tolerance}, got {max_score}"
    
    # Text similarity for string results
    if 'text' in expected and records:
        actual_text = str(records[0])  # Convert first record to string
        expected_text = expected['text']
        
        similarity = fuzz.ratio(actual_text, expected_text)
        assert similarity >= 80, \
            f"{test_id}: Text similarity too low ({similarity}%). Expected similar to: {expected_text}"


def extract_scores(records: List[Any]) -> List[float]:
    """Extract numeric score values from query results"""
    scores = []
    
    for record in records:
        # Handle different result formats
        if hasattr(record, 'get'):
            # Check common score field names
            for field in ['score', 'relevance_score', 'max_score', 'meilleur_score']:
                if field in record:
                    scores.append(float(record[field]))
                    break
    
    return scores


@pytest.mark.benchmark(group="eval-queries")
def test_eval_performance(eval_case, neo4j_session, benchmark):
    """
    Benchmark EVAL query performance using pytest-benchmark.
    
    This provides:
    - Statistical analysis (mean, median, stddev)
    - Comparison between runs
    - JSON export for tracking
    """
    query = eval_case.query
    
    def run_query():
        result = neo4j_session.run(query)
        # Must consume results for accurate timing
        records = list(result)
        summary = result.consume()
        return len(records), summary.result_available_after
    
    # Run benchmark (multiple iterations for statistics)
    result = benchmark(run_query)
    row_count, server_ms = result
    
    # Add metadata to benchmark
    benchmark.extra_info['query_id'] = eval_case.id
    benchmark.extra_info['category'] = eval_case.metadata.get('Category', 'Unknown')
    benchmark.extra_info['row_count'] = row_count
    benchmark.extra_info['server_ms'] = server_ms


@pytest.mark.slow
def test_eval_performance_threshold(eval_case, neo4j_session):
    """
    Test that queries meet performance thresholds.
    Mark slow tests explicitly for optional execution.
    """
    query = eval_case.query
    category = eval_case.metadata.get('Category', '')
    
    # Define thresholds by category
    thresholds = {
        'Search': 500,      # 500ms for search queries
        'Aggregation': 1000,  # 1s for aggregations
        'Graph': 2000,      # 2s for graph traversals
        'default': 1000     # 1s default
    }
    
    threshold_ms = thresholds.get(category, thresholds['default'])
    
    # Measure execution time
    start = time.perf_counter()
    result = neo4j_session.run(query)
    _ = list(result)  # Consume
    elapsed_ms = (time.perf_counter() - start) * 1000
    
    assert elapsed_ms < threshold_ms, \
        f"{eval_case.id}: Query too slow ({elapsed_ms:.0f}ms > {threshold_ms}ms threshold)"
```

### 4. Add Dependencies

Add to `requirements-test.txt` (or create if doesn't exist):

```txt
# Testing framework
pytest>=7.0.0
pytest-benchmark>=4.0.0

# Neo4j driver (reuse existing version)
neo4j>=5.0.0

# Markdown parsing
mistune>=3.0.0

# Text similarity
rapidfuzz>=3.0.0
```

### 5. Create `tests/README.md` for Usage Documentation

```markdown
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

# Run benchmarks only
pytest tests/test_eval_queries.py::test_eval_performance -v --benchmark-only

# Export benchmark data
pytest tests/test_eval_queries.py::test_eval_performance --benchmark-json=benchmark.json

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
```

### 6. Example EVAL File Structure (for reference)

```markdown
<!--- META: machine-readable for scripts --->
Status: PASSED
Category: Search
Duration-ms: —

# EVAL-02: Fred discute-t-il de ses projets de voyage?

### Query
```cypher
CALL db.index.fulltext.queryNodes('ContentFullText', 'Fred travel plans')
YIELD node, score
MATCH (node)<-[:HAS_CONTENT]-(s:Session)
RETURN count(*) as discussions_voyage,
       max(score) as meilleur_score
```

### Actual Result
```
discussions_voyage: 25
meilleur_score: 5.895384311676025
```
```

## Testing Strategy

1. **Unit tests** for parser with sample markdown
2. **Integration tests** against actual EVAL files
3. **Performance baseline** from initial run
4. **CI integration** to catch regressions

## Command Reference

```bash
# First time setup
cd neo4j-for-surveillance-poc-3
pip install -r requirements-test.txt

# Basic test run (functional only)
pytest tests/test_eval_queries.py::test_eval_functional -v

# Performance benchmarks
pytest tests/test_eval_queries.py::test_eval_performance -v --benchmark-only

# Full test suite
pytest tests/test_eval_queries.py -v

# Debug specific test
pytest tests/test_eval_queries.py::test_eval_functional[EVAL-02] -v -s

# Export results
pytest tests/test_eval_queries.py --benchmark-json=results.json --json-report --json-report-file=report.json
```

## Verification Commands

After implementation, verify with:

```bash
# 1. Check parser works standalone
python tests/eval_parser.py

# 2. Verify test discovery
pytest tests/test_eval_queries.py --collect-only

# 3. Run single test
pytest tests/test_eval_queries.py::test_eval_functional[EVAL-02] -v

# 4. Check benchmark output
pytest tests/test_eval_queries.py::test_eval_performance[EVAL-02] -v --benchmark-only
```

## Risks & Considerations

- **Parser fragility**: Mitigated by AST + regex fallback
- **Performance variance**: Use statistical analysis from pytest-benchmark
- **Breaking changes**: Test against Neo4j 5.x versions
- **Large datasets**: May need timeout configuration
- **Expected value changes**: Design allows easy updates to EVAL files

## Implementation Checklist

- [ ] Create `tests/eval_parser.py` with complete code above
- [ ] Add imports and pytest_generate_tests to `tests/conftest.py`
- [ ] Create `tests/test_eval_queries.py` with all test functions
- [ ] Add dependencies to `requirements-test.txt`
- [ ] Create `tests/README.md` documentation
- [ ] Run verification commands
- [ ] Commit with message: "feat: unified test framework for EVAL queries"
