#!/usr/bin/env python3
"""
Test dataset-specific Neo4j containers functionality.

This validates the acceptance criteria for issue #26.
"""

import subprocess
import time

import pytest


def run_command(cmd):
    """Execute shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def container_exists(name):
    """Check if a container exists (running or stopped)."""
    code, stdout, _ = run_command(f"docker ps -a --format '{{{{.Names}}}}' | grep -q '^{name}$'")
    return code == 0


def container_running(name):
    """Check if a container is running."""
    code, stdout, _ = run_command(f"docker ps --format '{{{{.Names}}}}' | grep -q '^{name}$'")
    return code == 0


def wait_for_neo4j(container_name, timeout=30):
    """Wait for Neo4j to be ready to accept connections."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        code, stdout, stderr = run_command(
            f"docker exec {container_name} cypher-shell -u neo4j -p 'Sup3rSecur3!' 'RETURN 1'"
        )
        if code == 0:
            return True
        time.sleep(1)
    return False


class TestDatasetContainers:
    """Test dataset-specific Neo4j container functionality."""

    @classmethod
    def setup_class(cls):
        """Ensure clean state before tests."""
        # Stop and remove any test containers
        for container in ["neo4j-default", "neo4j-bigdata", "neo4j-test"]:
            run_command(f"docker stop {container} 2>/dev/null")
            run_command(f"docker rm {container} 2>/dev/null")

    def test_fresh_start_creates_container(self):
        """AC1: No container on port 7474 -> run_neo4j.sh default -> neo4j-default starts."""
        # Given: No container on port 7474
        code, stdout, _ = run_command("docker ps --filter publish=7474 --format '{{.Names}}'")
        assert stdout.strip() == "", "Port 7474 should be free"

        # When: Run ./scripts/run-neo4j.sh default
        code, stdout, stderr = run_command("./scripts/run-neo4j.sh default")
        assert code == 0, f"Script failed: {stderr}"

        # Then: Container neo4j-default starts on 7474/7687
        assert container_running("neo4j-default"), "neo4j-default should be running"
        assert wait_for_neo4j("neo4j-default"), "Neo4j should be ready"

    def test_data_persistence_across_restart(self):
        """AC2/AC4: Data survives docker stop/start."""
        # Ensure container is running
        if not container_running("neo4j-default"):
            run_command("./scripts/run-neo4j.sh default")
            wait_for_neo4j("neo4j-default")

        # Create test data
        code, stdout, _ = run_command(
            "docker exec neo4j-default cypher-shell -u neo4j -p 'Sup3rSecur3!' "
            "'CREATE (n:TestNode {name: \"persistence-test\"}) RETURN n.name'"
        )
        assert code == 0, "Failed to create test data"

        # Stop and restart container
        run_command("docker stop neo4j-default")
        assert not container_running("neo4j-default"), "Container should be stopped"

        run_command("docker start neo4j-default")
        assert container_running("neo4j-default"), "Container should be running again"
        assert wait_for_neo4j("neo4j-default"), "Neo4j should be ready after restart"

        # Verify data persists
        code, stdout, _ = run_command(
            "docker exec neo4j-default cypher-shell -u neo4j -p 'Sup3rSecur3!' "
            "'MATCH (n:TestNode {name: \"persistence-test\"}) RETURN n.name'"
        )
        assert code == 0, "Failed to query test data"
        assert "persistence-test" in stdout, "Data should persist across restart"

    def test_dataset_switching(self):
        """AC3: Running container -> run_neo4j.sh bigdata -> auto-stops and starts new."""
        # Given: neo4j-default is running
        if not container_running("neo4j-default"):
            run_command("./scripts/run-neo4j.sh default")
            wait_for_neo4j("neo4j-default")

        # When: Run ./scripts/run-neo4j.sh bigdata
        code, stdout, stderr = run_command("./scripts/run-neo4j.sh bigdata")
        assert code == 0, f"Script failed: {stderr}"

        # Then: neo4j-default stopped, neo4j-bigdata running
        assert not container_running("neo4j-default"), "neo4j-default should be stopped"
        assert container_running("neo4j-bigdata"), "neo4j-bigdata should be running"
        assert wait_for_neo4j("neo4j-bigdata"), "Neo4j bigdata should be ready"

    def test_existing_container_restart(self):
        """AC5: Existing container -> rerun script -> starts existing (not error)."""
        # Ensure neo4j-test exists but is stopped
        if not container_exists("neo4j-test"):
            run_command("./scripts/run-neo4j.sh test")
            wait_for_neo4j("neo4j-test")
        run_command("docker stop neo4j-test")

        # When: Rerun ./scripts/run-neo4j.sh test
        code, stdout, stderr = run_command("./scripts/run-neo4j.sh test")
        assert code == 0, f"Script should handle existing container: {stderr}"
        assert "Starting existing container" in stdout, "Should restart existing container"

        # Then: Container should be running
        assert container_running("neo4j-test"), "neo4j-test should be running"

    def test_no_hardcoded_references(self):
        """AC8: No neo4j-sessions literals remain in code."""
        # Check for neo4j-sessions in non-eval files
        code, stdout, _ = run_command(
            "rg -l 'neo4j-sessions' . --type md --type sh --type py --type cypher | grep -v 'evals/' | grep -v '.git'"
        )

        if stdout.strip():
            files_with_literals = stdout.strip().split("\n")
            pytest.fail(f"Found neo4j-sessions literals in: {files_with_literals}")

    @classmethod
    def teardown_class(cls):
        """Clean up test containers."""
        for container in ["neo4j-default", "neo4j-bigdata", "neo4j-test"]:
            run_command(f"docker stop {container} 2>/dev/null")
            run_command(f"docker rm {container} 2>/dev/null")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
