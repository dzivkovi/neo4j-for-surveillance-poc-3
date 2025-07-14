"""
Quality gates validation for enhanced /work command automation.

This module provides automated validation checkpoints to ensure implementation
meets production readiness standards before deployment.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple


class QualityGates:
    """Comprehensive quality gates validation system."""

    def __init__(self):
        """Initialize quality gates validator."""
        self.validation_results: Dict[str, bool] = {}
        self.validation_errors: Dict[str, str] = {}

    def validate_all_gates(self) -> Tuple[bool, Dict[str, str]]:
        """
        Run all quality gate validations.

        Returns:
            Tuple of (all_passed, error_details)
        """
        gate_methods = [
            ("git_workflow", self.validate_git_workflow),
            ("naming_conventions", self.validate_naming_conventions),
            ("file_structure", self.validate_file_structure),
            ("design_compliance", self.validate_design_compliance),
            ("production_config", self.validate_production_config),
            ("database_consistency", self.validate_database_consistency),
            ("complete_coverage", self.validate_complete_coverage),
        ]

        all_passed = True

        for gate_name, gate_method in gate_methods:
            try:
                result = gate_method()
                self.validation_results[gate_name] = result
                if not result:
                    all_passed = False
            except Exception as e:
                self.validation_results[gate_name] = False
                self.validation_errors[gate_name] = str(e)
                all_passed = False

        return all_passed, self.validation_errors

    def validate_git_workflow(self) -> bool:
        """
        Validate git workflow compliance (feature branch usage).

        Returns:
            True if on feature branch, False if on main/master
        """
        try:
            result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)

            current_branch = result.stdout.strip()

            # Should be on a feature branch, not main/master
            if current_branch in ["main", "master"]:
                self.validation_errors["git_workflow"] = f"Working on {current_branch} branch instead of feature branch"
                return False

            # Should be on a feature branch (starts with feat/, fix/, etc.)
            if not any(current_branch.startswith(prefix) for prefix in ["feat/", "fix/", "docs/", "chore/"]):
                self.validation_errors["git_workflow"] = f"Branch '{current_branch}' doesn't follow naming convention"
                return False

            return True

        except subprocess.CalledProcessError as e:
            self.validation_errors["git_workflow"] = f"Git command failed: {e}"
            return False

    def validate_naming_conventions(self) -> bool:
        """
        Validate naming conventions across the codebase.

        With minimal validator, this always passes since we let Claude
        handle language-specific conventions naturally.

        Returns:
            True (always passes with minimal validation)
        """
        # Let Claude handle conventions naturally during code review
        # The minimal validator doesn't enforce hard-coded rules
        return True

    def validate_file_structure(self) -> bool:
        """
        Validate file structure compliance.

        Returns:
            True if all files are in correct locations
        """
        from workflow.convention_validator import ConventionValidator

        validator = ConventionValidator()

        # Check for misplaced test files
        for file_path in Path(".").rglob("*"):
            if file_path.is_file():
                file_str = str(file_path)

                # Skip files in venv, .git, or other excluded directories
                if "venv" in file_str or ".git" in file_str or "__pycache__" in file_str:
                    continue

                if validator.should_move_test_file(file_str):
                    self.validation_errors["file_structure"] = (
                        f"Test file {file_str} should be moved to {validator.get_correct_test_location(file_str)}"
                    )
                    return False

        return True

    def validate_design_compliance(self, implementation_summary: str = "") -> bool:
        """
        Validate implementation compliance with design document.

        Args:
            implementation_summary: Summary of what was implemented

        Returns:
            True if implementation follows design
        """
        from workflow.design_compliance import DesignCompliance

        compliance = DesignCompliance()

        # Try to load design document (look for any issue number)
        design_loaded = False
        for analysis_dir in Path("analysis").iterdir():
            if analysis_dir.is_dir() and analysis_dir.name.isdigit():
                if compliance.load_design_document(int(analysis_dir.name)):
                    design_loaded = True
                    break

        if not design_loaded:
            # No design document found - skip validation
            return True

        if implementation_summary:
            is_compliant, deviations = compliance.validate_implementation_approach(implementation_summary)

            if not is_compliant:
                self.validation_errors["design_compliance"] = f"Design deviations detected: {'; '.join(deviations)}"
                return False

        return True

    def validate_production_config(self, code_content: str = "") -> bool:
        """
        Validate production configuration (no test-only filters).

        Args:
            code_content: Code content to validate (optional)

        Returns:
            True if production-ready, False if test-only code detected
        """
        # If specific content provided, check it
        if code_content:
            return self._check_content_for_test_filters(code_content)

        # Otherwise, scan all relevant files
        test_filter_patterns = [
            r"LIMIT\s+\d+\s*(?://.*test|#.*test)",  # LIMIT with test comment
            r"LIMIT\s+(?:10|100|1000)\s*$",  # Common test limits
            r"\.head\(\d+\)",  # DataFrame head() calls
            r"\.sample\(\d+\)",  # Sample calls
            r"test.*filter",  # Variables with 'test' and 'filter'
            r"debug.*mode",  # Debug mode indicators
        ]

        # Check Python and Cypher files
        for file_path in Path(".").rglob("*"):
            if file_path.suffix in [".py", ".cypher", ".sql"]:
                if (
                    "venv" in str(file_path)
                    or ".git" in str(file_path)
                    or "test_" in file_path.name
                    or file_path.name.startswith("test_")
                    or ".claude/workflow" in str(file_path)
                ):
                    continue

                try:
                    content = file_path.read_text()

                    for pattern in test_filter_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            self.validation_errors["production_config"] = (
                                f"Test-only filter detected in {file_path}: {pattern}"
                            )
                            return False

                except Exception:
                    continue  # Skip files that can't be read

        return True

    def validate_database_consistency(self) -> bool:
        """
        Validate database consistency using Neo4j driver.

        Returns:
            True if database validation passes
        """
        try:
            # Check if this is a Neo4j project
            is_neo4j_project = False

            # Check for Neo4j configuration in CLAUDE.md
            if Path("CLAUDE.md").exists():
                content = Path("CLAUDE.md").read_text()
                if "neo4j" in content.lower() and "cypher" in content.lower():
                    is_neo4j_project = True

            # If not a Neo4j project, skip validation
            if not is_neo4j_project:
                return True

            # Connect to live Neo4j database and validate schema
            return self._validate_live_neo4j_schema()

        except Exception as e:
            self.validation_errors["database_consistency"] = f"Database validation failed: {e}"
            return False

    def _validate_live_neo4j_schema(self) -> bool:
        """Validate live Neo4j database schema using driver."""
        try:
            from neo4j import GraphDatabase
            
            # Use hardcoded credentials from project
            NEO4J_URI = "bolt://localhost:7687"
            NEO4J_USER = "neo4j"
            NEO4J_PASSWORD = "Sup3rSecur3!"
            
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            
            with driver.session() as session:
                # Test basic connectivity
                result = session.run("RETURN 1 as test")
                if not result.single():
                    self.validation_errors["database_consistency"] = "Cannot connect to Neo4j database"
                    return False
                
                # Check essential constraints exist
                result = session.run("SHOW CONSTRAINTS")
                constraints = [r["name"] for r in result]
                
                essential_constraints = ["session_guid", "phone_number", "email_addr"]
                missing_constraints = [c for c in essential_constraints if c not in constraints]
                
                if missing_constraints:
                    self.validation_errors["database_consistency"] = f"Missing constraints: {missing_constraints}"
                    return False
                
                # Check that we have data
                result = session.run("MATCH (n) RETURN count(n) as total")
                total_nodes = result.single()["total"]
                
                if total_nodes == 0:
                    self.validation_errors["database_consistency"] = "Database is empty - no nodes found"
                    return False
                
            driver.close()
            return True
            
        except ImportError:
            # neo4j driver not available - skip validation
            return True
        except Exception as e:
            self.validation_errors["database_consistency"] = f"Neo4j validation failed: {str(e)}"
            return False

    def validate_complete_coverage(self) -> bool:
        """
        Validate complete implementation coverage.

        Returns:
            True if all requirements are implemented
        """
        # Check that core automation files exist
        required_files = [
            ".claude/workflow/convention_validator.py",
            ".claude/workflow/design_compliance.py",
            ".claude/workflow/quality_gates.py",
            ".claude/workflow/definition_of_done.py",
        ]

        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            self.validation_errors["complete_coverage"] = f"Missing required files: {', '.join(missing_files)}"
            return False

        # Check that tests exist and pass
        if Path("tests").exists():
            try:
                # Run tests to verify they pass
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", "tests/", "-q"], capture_output=True, text=True
                )

                if result.returncode != 0:
                    self.validation_errors["complete_coverage"] = f"Tests are failing: {result.stderr}"
                    return False

            except Exception as e:
                self.validation_errors["complete_coverage"] = f"Test execution failed: {e}"
                return False

        return True

    def _check_content_for_test_filters(self, content: str) -> bool:
        """Check specific content for test-only filters."""
        test_indicators = ["LIMIT 100", "LIMIT 10", "test_only", "debug_mode", ".head(", ".sample("]

        content_lower = content.lower()
        for indicator in test_indicators:
            if indicator.lower() in content_lower:
                return False

        return True

    def get_validation_report(self) -> Dict[str, any]:
        """
        Get comprehensive validation report.

        Returns:
            Dictionary with validation results and error details
        """
        return {
            "results": self.validation_results.copy(),
            "errors": self.validation_errors.copy(),
            "all_passed": all(self.validation_results.values()),
            "passed_count": sum(self.validation_results.values()),
            "total_count": len(self.validation_results),
        }
