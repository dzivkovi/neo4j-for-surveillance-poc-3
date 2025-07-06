#!/usr/bin/env python3
"""Test direct Neo4j connection for confidence generation"""


import pytest
from neo4j import GraphDatabase

# Connection details from CLAUDE.md
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Sup3rSecur3!"


@pytest.fixture(scope="module")
def neo4j_driver():
    """Create Neo4j driver for tests"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    yield driver
    driver.close()


@pytest.fixture
def neo4j_session(neo4j_driver):
    """Create a session for each test"""
    session = neo4j_driver.session()
    yield session
    session.close()


class TestNeo4jConnection:
    """Test direct Neo4j database connection capabilities"""

    def test_basic_connection(self, neo4j_session):
        """Test basic connection to Neo4j"""
        result = neo4j_session.run("RETURN 1 as test")
        record = result.single()
        assert record["test"] == 1, "Basic connection query should return 1"

    def test_schema_access(self, neo4j_session):
        """Test ability to query database schema"""
        result = neo4j_session.run("CALL db.labels()")
        labels = [record["label"] for record in result]

        # Expected labels from POLE schema
        expected_labels = {"Session", "Person", "Phone", "Email", "Content"}
        actual_labels = set(labels)

        assert expected_labels.issubset(actual_labels), f"Missing expected labels. Found: {actual_labels}"

    def test_fulltext_search(self, neo4j_session):
        """Test full-text search capability (used in many eval tests)"""
        query = """
        CALL db.index.fulltext.queryNodes('ContentFullText', 'travel plans')
        YIELD node, score
        RETURN count(node) as match_count
        """
        result = neo4j_session.run(query)
        record = result.single()

        assert record is not None, "Full-text search should return results"
        assert record["match_count"] >= 0, "Match count should be non-negative"

    def test_evaluation_query_pattern(self, neo4j_session):
        """Test execution of evaluation-style query with count and score"""
        # EVAL-03 style query
        query = """
        CALL db.index.fulltext.queryNodes('ContentFullText', '@Merlin, Fred travel plans')
        YIELD node, score
        MATCH (node)<-[:HAS_CONTENT]-(s:Session)
        RETURN count(DISTINCT s) as session_count, 
               max(score) as max_score
        """
        result = neo4j_session.run(query)
        record = result.single()

        assert record is not None, "Query should return results"
        assert record["session_count"] is not None, "Should have session_count field"
        assert record["max_score"] is not None, "Should have max_score field"
        assert isinstance(record["session_count"], int), "Count should be integer"
        assert isinstance(record["max_score"], (int, float)), "Score should be numeric"

    def test_query_with_parameters(self, neo4j_session):
        """Test parameterized query execution"""
        query = """
        MATCH (p:Person)
        WHERE p.name CONTAINS $name_part
        RETURN count(p) as person_count
        """
        result = neo4j_session.run(query, name_part="Fred")
        record = result.single()

        assert record is not None, "Parameterized query should return results"
        assert record["person_count"] >= 0, "Should find persons"

    def test_query_error_handling(self, neo4j_session):
        """Test handling of invalid queries"""
        with pytest.raises(Exception):
            # Invalid Cypher syntax
            neo4j_session.run("MATCH (n:InvalidSyntax")

    def test_transaction_rollback(self, neo4j_session):
        """Test that read-only queries don't modify database"""
        # Count nodes before
        result = neo4j_session.run("MATCH (n) RETURN count(n) as count")
        count_before = result.single()["count"]

        # Run read query
        neo4j_session.run("MATCH (n:Session) RETURN n LIMIT 10")

        # Count nodes after
        result = neo4j_session.run("MATCH (n) RETURN count(n) as count")
        count_after = result.single()["count"]

        assert count_before == count_after, "Read queries should not modify database"


class TestQueryResultExtraction:
    """Test extraction of count/score from query results for confidence calculation"""

    @staticmethod
    def extract_confidence_data(session, query):
        """Helper to execute query and extract count/score for confidence calculation"""
        result = session.run(query)
        record = result.single()

        if record:
            data = dict(record)

            # Look for count-like fields
            count_fields = [
                k for k in data.keys() if "count" in k.lower() or k in ["discussions_voyage", "shed_sessions"]
            ]
            count = data[count_fields[0]] if count_fields else None

            # Look for score-like fields
            score_fields = [k for k in data.keys() if "score" in k.lower()]
            score = float(data[score_fields[0]]) if score_fields else None

            return {"count": count, "score": score, "raw": data}
        return None

    def test_extract_eval02_pattern(self, neo4j_session):
        """Test extraction from EVAL-02 French query pattern"""
        query = """
        CALL db.index.fulltext.queryNodes('ContentFullText', 'Fred travel', {analyzer:'standard'})
        YIELD node, score
        MATCH (node)<-[:HAS_CONTENT]-(s:Session)
        RETURN count(*) as discussions_voyage,
               max(score) as meilleur_score
        """

        result = self.extract_confidence_data(neo4j_session, query)
        assert result is not None, "Should extract data from EVAL-02 pattern"
        assert "count" in result, "Should extract count"
        assert "score" in result, "Should extract score"
        assert isinstance(result["count"], int), "Count should be integer"
        assert isinstance(result["score"], float), "Score should be float"

    def test_extract_eval06_pattern(self, neo4j_session):
        """Test extraction from EVAL-06 shed query pattern"""
        query = """
        MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
        WHERE c.text CONTAINS 'shed'
        RETURN count(DISTINCT s) as shed_sessions,
               1.0 as relevance_score
        """

        result = self.extract_confidence_data(neo4j_session, query)
        assert result is not None, "Should extract data from EVAL-06 pattern"
        assert result["raw"]["shed_sessions"] == result["count"], "Should map shed_sessions to count"

    def test_calculate_confidence(self):
        """Test confidence calculation formula"""
        # Test data from EVAL-02
        expected_count = 25
        actual_count = 25
        expected_score = 5.90
        actual_score = 5.89

        count_accuracy = min(actual_count, expected_count) / expected_count
        score_similarity = max(0, 1 - abs(actual_score - expected_score) / expected_score)
        confidence = (count_accuracy * 0.7) + (score_similarity * 0.3)

        assert confidence >= 0.99, f"Confidence should be high for near-perfect match: {confidence}"

        # Test with less perfect match
        actual_count = 20
        count_accuracy = min(actual_count, expected_count) / expected_count
        confidence = (count_accuracy * 0.7) + (score_similarity * 0.3)

        assert 0.5 < confidence < 0.9, f"Confidence should be moderate for partial match: {confidence}"


@pytest.mark.integration
class TestEvaluationQueries:
    """Test actual evaluation queries from the test suite"""

    def test_eval_03_query(self, neo4j_session):
        """Test EVAL-03: Does <@Merlin, Fred> discuss travel plans?"""
        query = """
        CALL db.index.fulltext.queryNodes('ContentFullText', '@Merlin, Fred travel plans')
        YIELD node, score
        MATCH (node)<-[:HAS_CONTENT]-(s:Session)
        WITH s, node, score
        OPTIONAL MATCH (s)<-[:PARTICIPATED_IN]-()<-[:USES]-(p:Person)
        WHERE p.name = '@Merlin, Fred'
        WITH s, score, p
        WHERE p IS NOT NULL
        RETURN count(DISTINCT s) as travel_discussions,
               max(score) as relevance_score
        """

        result = neo4j_session.run(query)
        record = result.single()

        assert record is not None, "EVAL-03 query should return results"
        assert record["travel_discussions"] >= 0, "Should have non-negative discussion count"
        assert record["relevance_score"] > 0, "Should have positive relevance score"
