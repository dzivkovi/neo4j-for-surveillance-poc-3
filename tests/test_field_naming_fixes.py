#!/usr/bin/env python
"""
Test cases for field naming fixes and computed enrichments (Issue #34)

These tests verify:
1. stoptime is correctly imported (not endtime)
2. durationinseconds is computed when missing
3. sessiondate is computed from starttime
4. No endtime references exist in codebase
"""

import json
import pathlib
import subprocess
from datetime import datetime

import pytest
from neo4j import GraphDatabase

# Neo4j connection details
BOLT_URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Sup3rSecur3!")


@pytest.fixture
def neo4j_driver():
    """Create Neo4j driver for tests"""
    driver = GraphDatabase.driver(BOLT_URI, auth=AUTH)
    yield driver
    driver.close()


def test_no_endtime_references_in_codebase():
    """Regression test: Ensure no 'endtime' references exist in scripts or queries"""
    # Search for endtime in all Python and Cypher files
    result = subprocess.run(
        ["grep", "-r", "endtime", "scripts/", "queries/"],
        capture_output=True,
        text=True
    )
    
    # Filter out this test file itself
    lines = [line for line in result.stdout.split('\n') 
             if line and 'test_field_naming_fixes.py' not in line]
    
    assert len(lines) == 0, f"Found 'endtime' references:\n{chr(10).join(lines)}"


def test_stoptime_correctly_imported(neo4j_driver):
    """Test that stoptime is correctly populated from source data"""
    # Create a minimal test session with stoptime
    test_session = {
        "sessionguid": "test-stoptime-001",
        "sessiontype": "Telephony",
        "starttime": "2020-02-15T10:00:00Z",
        "endtime": "2020-02-15T10:05:00Z",  # This is what's in source data
        "involvements": []
    }
    
    # Import using the fixed script (will fail initially)
    # After fix, this should map endtime -> stoptime
    with neo4j_driver.session() as session:
        # Clean up any existing test data
        session.run("MATCH (s:Session {sessionguid: $guid}) DETACH DELETE s", 
                   guid=test_session["sessionguid"])
        
        # The import logic should be fixed to map endtime -> stoptime
        # This will fail until we fix the import script
        result = session.run(
            "MATCH (s:Session {sessionguid: $guid}) RETURN s.stoptime as stoptime",
            guid=test_session["sessionguid"]
        ).single()
        
        assert result is not None, "Session should have stoptime field"
        assert result["stoptime"] is not None, "stoptime should not be null"


def test_duration_computed_when_missing(neo4j_driver):
    """Test that durationinseconds is computed from stoptime - starttime when missing"""
    test_session = {
        "sessionguid": "test-duration-001",
        "sessiontype": "Telephony", 
        "starttime": "2020-02-15T10:00:00Z",
        "endtime": "2020-02-15T10:05:00Z",  # 5 minutes = 300 seconds
        # Note: no durationinseconds in source
        "involvements": []
    }
    
    # After import with fixes
    with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (s:Session {sessionguid: $guid}) 
            RETURN s.durationinseconds as duration
            """,
            guid=test_session["sessionguid"]
        ).single()
        
        assert result is not None
        assert result["duration"] == 300, "Duration should be 300 seconds (5 minutes)"


def test_sessiondate_computed_from_starttime(neo4j_driver):
    """Test that sessiondate is computed from starttime for temporal queries"""
    test_session = {
        "sessionguid": "test-sessiondate-001",
        "sessiontype": "Email",
        "starttime": "2020-02-15T10:30:45Z",
        "involvements": []
    }
    
    # After import with fixes
    with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (s:Session {sessionguid: $guid}) 
            RETURN s.sessiondate as sessiondate, date(s.starttime) as expected_date
            """,
            guid=test_session["sessionguid"]
        ).single()
        
        assert result is not None
        assert result["sessiondate"] is not None, "sessiondate should be computed"
        assert result["sessiondate"] == result["expected_date"], \
            "sessiondate should match date(starttime)"


def test_all_sessions_have_stoptime_after_import(neo4j_driver):
    """Test that all imported sessions have stoptime values where source has endtime"""
    with neo4j_driver.session() as session:
        # Count sessions missing stoptime
        result = session.run(
            """
            MATCH (s:Session)
            WHERE s.starttime IS NOT NULL 
            AND s.stoptime IS NULL
            RETURN count(s) as missing_stoptime_count
            """
        ).single()
        
        assert result["missing_stoptime_count"] == 0, \
            f"Found {result['missing_stoptime_count']} sessions without stoptime"


def test_audio_duration_estimation():
    """Test that audio duration can be estimated from WAV file size"""
    # WAV file: 44.1kHz, 16-bit, mono = 88,200 bytes/second
    # This is a placeholder for the actual implementation
    wav_size_bytes = 882000  # 10 seconds of audio
    expected_duration = 10
    
    # This will be implemented in the import script
    # estimated_duration = estimate_wav_duration(wav_size_bytes)
    # assert estimated_duration == expected_duration
    pass  # Marked as [S]mall scope in design doc


if __name__ == "__main__":
    # Run tests 5+ times to catch any nondeterminism
    for i in range(5):
        print(f"\nTest run {i+1}/5")
        pytest.main([__file__, "-v"])