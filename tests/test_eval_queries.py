"""
Test suite for EVAL queries - functional and performance testing.
Automatically runs all queries from evals/passed/EVAL-*.md files.
"""

import time
from typing import Any

import pytest
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


def validate_results(records: list[Any], expected: dict, test_id: str):
    """
    Validate query results against expected values.
    Supports count validation, score validation, and text similarity.
    """
    # For queries that return aggregated results (single row with count field)
    if "count" in expected and records and len(records) == 1:
        record = records[0]
        # Check if the record has a count-like field
        count_fields = ["discussions_voyage", "shed_sessions", "travel_discussions", "session_count", "count", "total"]
        for field in count_fields:
            if field in record:
                actual_count = record[field]
                expected_count = expected["count"]

                # Allow 10% tolerance for counts
                tolerance = max(1, int(expected_count * 0.1))
                assert abs(actual_count - expected_count) <= tolerance, (
                    f"{test_id}: Expected {field}={expected_count}±{tolerance}, got {actual_count}"
                )
                break
    # For queries that return multiple rows
    elif "count" in expected:
        actual_count = len(records)
        expected_count = expected["count"]

        # Allow 10% tolerance for counts
        tolerance = max(1, int(expected_count * 0.1))
        assert abs(actual_count - expected_count) <= tolerance, (
            f"{test_id}: Expected {expected_count}±{tolerance} rows, got {actual_count}"
        )

    # Score validation (if query returns scores)
    if "score" in expected and records:
        # Extract numeric scores from results
        scores = extract_scores(records)
        if scores:
            max_score = max(scores)
            expected_score = float(expected["score"])

            # Allow 20% tolerance for scores
            tolerance = expected_score * 0.2
            assert abs(max_score - expected_score) <= tolerance, (
                f"{test_id}: Expected score {expected_score}±{tolerance}, got {max_score}"
            )

    # Text similarity for string results
    if "text" in expected and records:
        actual_text = str(records[0])  # Convert first record to string
        expected_text = expected["text"]

        similarity = fuzz.ratio(actual_text, expected_text)
        assert similarity >= 80, (
            f"{test_id}: Text similarity too low ({similarity}%). Expected similar to: {expected_text}"
        )


def extract_scores(records: list[Any]) -> list[float]:
    """Extract numeric score values from query results"""
    scores = []

    for record in records:
        # Check common score field names
        for field in ["score", "relevance_score", "max_score", "meilleur_score"]:
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
    benchmark.extra_info["query_id"] = eval_case.id
    benchmark.extra_info["category"] = eval_case.metadata.get("Category", "Unknown")
    benchmark.extra_info["row_count"] = row_count
    benchmark.extra_info["server_ms"] = server_ms


@pytest.mark.slow
def test_eval_performance_threshold(eval_case, neo4j_session):
    """
    Test that queries meet performance thresholds.
    Mark slow tests explicitly for optional execution.
    """
    query = eval_case.query
    category = eval_case.metadata.get("Category", "")

    # Define thresholds by category
    thresholds = {
        "Search": 500,  # 500ms for search queries
        "Aggregation": 1000,  # 1s for aggregations
        "Graph": 2000,  # 2s for graph traversals
        "default": 1000,  # 1s default
    }

    threshold_ms = thresholds.get(category, thresholds["default"])

    # Measure execution time
    start = time.perf_counter()
    result = neo4j_session.run(query)
    _ = list(result)  # Consume
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert elapsed_ms < threshold_ms, (
        f"{eval_case.id}: Query too slow ({elapsed_ms:.0f}ms > {threshold_ms}ms threshold)"
    )
