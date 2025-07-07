"""
Pytest configuration and fixtures for Neo4j testing.
"""

import os
from pathlib import Path

import pytest
from eval_parser import parse_eval_files
from neo4j import GraphDatabase

# Cache for performance
_TEST_CASES = None


@pytest.fixture(scope="session")
def neo4j_driver():
    """Create Neo4j driver instance for the test session."""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "Sup3rSecur3!")

    driver = GraphDatabase.driver(uri, auth=(user, password))

    # Verify connectivity
    try:
        driver.verify_connectivity()
    except Exception as e:
        pytest.skip(f"Neo4j connection failed: {e}")

    yield driver
    driver.close()


@pytest.fixture(scope="session")
def neo4j_session(neo4j_driver):
    """Create a Neo4j session for queries."""
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    with neo4j_driver.session(database=database) as session:
        yield session


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
        metafunc.parametrize("eval_case", _TEST_CASES, ids=[case.id for case in _TEST_CASES])
