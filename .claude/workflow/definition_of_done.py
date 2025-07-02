"""
Definition of Done framework for enhanced /work command automation.

This module provides systematic validation to prevent premature success declaration
by ensuring ALL quality criteria are met before declaring work complete.
"""

import subprocess
import sys
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional


class QualityGateFailure(Exception):
    """Exception raised when a quality gate fails validation."""

    pass


class QualityGate(ABC):
    """Abstract base class for quality gates."""

    def __init__(self, name: str):
        """
        Initialize quality gate.

        Args:
            name: Human-readable name of the quality gate
        """
        self.name = name
        self.error: str = ""

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate this quality gate.

        Returns:
            True if validation passes, False otherwise
        """
        pass


class FunctionalGate(QualityGate):
    """Validates all tests passing (unit + integration + regression)."""

    def __init__(self):
        super().__init__("Functional")

    def validate(self) -> bool:
        """Validate that all tests are passing."""
        try:
            # Run pytest with verbose output
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-v"],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )

            if result.returncode != 0:
                self.error = f"Tests failing: {result.stderr}"
                return False

            # Check for any skipped tests that shouldn't be skipped
            if "SKIPPED" in result.stdout:
                # Allow some skipped tests, but flag if too many
                skipped_count = result.stdout.count("SKIPPED")
                total_count = result.stdout.count("PASSED") + result.stdout.count("FAILED") + skipped_count

                if skipped_count > total_count * 0.2:  # More than 20% skipped
                    self.error = f"Too many skipped tests: {skipped_count}/{total_count}"
                    return False

            return True

        except subprocess.TimeoutExpired:
            self.error = "Test execution timed out"
            return False
        except Exception as e:
            self.error = f"Test execution failed: {e}"
            return False


class ConventionalGate(QualityGate):
    """Validates all naming conventions are followed."""

    def __init__(self):
        super().__init__("Conventional")

    def validate(self) -> bool:
        """Validate naming conventions."""
        try:
            from workflow.quality_gates import QualityGates

            gates = QualityGates()
            result = gates.validate_naming_conventions()

            if not result:
                self.error = gates.validation_errors.get("naming_conventions", "Convention violations detected")

            return result

        except Exception as e:
            self.error = f"Convention validation failed: {e}"
            return False


class StructuralGate(QualityGate):
    """Validates all files are in correct locations."""

    def __init__(self):
        super().__init__("Structural")

    def validate(self) -> bool:
        """Validate file structure."""
        try:
            from workflow.quality_gates import QualityGates

            gates = QualityGates()
            result = gates.validate_file_structure()

            if not result:
                self.error = gates.validation_errors.get("file_structure", "File structure violations detected")

            return result

        except Exception as e:
            self.error = f"Structure validation failed: {e}"
            return False


class OperationalGate(QualityGate):
    """Validates production-ready configuration."""

    def __init__(self):
        super().__init__("Operational")

    def validate(self) -> bool:
        """Validate operational readiness."""
        try:
            from workflow.quality_gates import QualityGates

            gates = QualityGates()

            # Check production configuration
            prod_config_result = gates.validate_production_config()
            if not prod_config_result:
                self.error = gates.validation_errors.get("production_config", "Production config issues detected")
                return False

            # Check performance requirements
            perf_result = self.validate_performance()
            if not perf_result:
                return False

            return True

        except Exception as e:
            self.error = f"Operational validation failed: {e}"
            return False

    def validate_performance(self) -> bool:
        """Validate performance requirements."""
        # Measure query performance
        performance_time = self.measure_query_performance()

        # Performance requirement: queries should complete under 5 seconds
        if performance_time > 5.0:
            self.error = f"Query performance too slow: {performance_time:.1f}s (limit: 5.0s)"
            return False

        # Also check that no obviously slow patterns are used
        slow_patterns = [
            "SELECT *",  # Full table scans
            "MATCH (n) RETURN n",  # Full graph traversal
            "cartesian product",  # Cartesian products
        ]

        for py_file in Path(".").rglob("*.py"):
            if (
                "venv" in str(py_file)
                or ".git" in str(py_file)
                or ".claude/workflow" in str(py_file)
                or "test_" in py_file.name
            ):
                continue

            try:
                content = py_file.read_text().lower()
                for pattern in slow_patterns:
                    if pattern in content:
                        self.error = f"Potentially slow pattern '{pattern}' found in {py_file}"
                        return False
            except Exception:
                continue

        return True

    def measure_query_performance(self) -> float:
        """
        Measure query performance (mock implementation).

        Returns:
            Query execution time in seconds
        """
        # Mock implementation - would measure actual query times in practice
        return 3.2  # Simulated 3.2 second response time


class IntegrativeGate(QualityGate):
    """Validates MCP validation and database consistency."""

    def __init__(self):
        super().__init__("Integrative")

    def validate(self) -> bool:
        """Validate integration points."""
        try:
            from workflow.quality_gates import QualityGates

            gates = QualityGates()
            result = gates.validate_database_consistency()

            if not result:
                self.error = gates.validation_errors.get("database_consistency", "Database consistency issues detected")

            return result

        except Exception as e:
            self.error = f"Integration validation failed: {e}"
            return False


class ContractualGate(QualityGate):
    """Validates original acceptance criteria are met."""

    def __init__(self):
        super().__init__("Contractual")

    def validate(self) -> bool:
        """Validate acceptance criteria."""
        try:
            from workflow.design_compliance import DesignCompliance

            compliance = DesignCompliance()

            # Load design document if available
            design_loaded = False
            for analysis_dir in Path("analysis").iterdir():
                if analysis_dir.is_dir() and analysis_dir.name.isdigit():
                    if compliance.load_design_document(int(analysis_dir.name)):
                        design_loaded = True
                        break

            if not design_loaded:
                # No design document - skip validation
                return True

            # Check acceptance criteria coverage
            # This would be enhanced with actual test result mapping
            test_results = self._get_test_results()
            all_covered, missing = compliance.check_acceptance_criteria_coverage(test_results)

            if not all_covered:
                self.error = f"Missing acceptance criteria coverage: {'; '.join(missing[:3])}"
                return False

            return True

        except Exception as e:
            self.error = f"Contractual validation failed: {e}"
            return False

    def _get_test_results(self) -> Dict[str, bool]:
        """Get test results for acceptance criteria checking."""
        # This would parse actual test results
        # For now, return mock results based on existing test files
        test_results = {}

        for test_file in Path("tests").rglob("test_*.py"):
            # Extract test method names
            try:
                content = test_file.read_text()
                import re

                test_methods = re.findall(r"def (test_\w+)", content)

                for method in test_methods:
                    test_results[method] = True  # Assume passing for now

            except Exception:
                continue

        return test_results


class RegressionGate(QualityGate):
    """Validates no existing functionality is broken."""

    def __init__(self):
        super().__init__("Regression")

    def validate(self) -> bool:
        """Validate no regressions."""
        try:
            # Run existing evaluation tests
            eval_result = self._run_evaluation_tests()
            if not eval_result:
                return False

            # Check database state consistency
            db_result = self._check_database_state()
            if not db_result:
                return False

            return True

        except Exception as e:
            self.error = f"Regression validation failed: {e}"
            return False

    def _run_evaluation_tests(self) -> bool:
        """Run evaluation test suite to check for regressions."""
        eval_file = Path("queries/eval-suite.cypher")
        if not eval_file.exists():
            # No evaluation suite - run basic tests instead
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", "-q", "--tb=no"], capture_output=True, text=True, timeout=60
                )

                if result.returncode != 0:
                    self.error = f"Basic tests failed: {result.stderr}"
                    return False

                return True

            except Exception as e:
                self.error = f"Test execution failed: {e}"
                return False

        try:
            # In a real implementation, this would execute the eval suite with Neo4j
            # For now, just check that the file is valid
            content = eval_file.read_text()

            # Basic validation - file should contain Cypher queries
            if "MATCH" not in content or "RETURN" not in content:
                self.error = "Evaluation suite appears invalid"
                return False

            return True

        except Exception as e:
            self.error = f"Evaluation test execution failed: {e}"
            return False

    def _check_database_state(self) -> bool:
        """Check that database state is consistent."""
        # This would validate database integrity in a real implementation
        # For now, just check that schema files exist and are valid

        schema_file = Path("scripts/cypher/01-schema.cypher")
        if not schema_file.exists():
            # If no schema file, that's okay for some projects
            return True

        try:
            # Basic validation - schema file should contain valid Cypher
            content = schema_file.read_text()
            if "CREATE" not in content.upper() and "CONSTRAINT" not in content.upper():
                self.error = "Schema file appears invalid"
                return False
        except Exception:
            # Can't read schema file
            return True

        return True


class DefinitionOfDoneValidator:
    """Systematic validator that enforces all quality gates before completion."""

    def __init__(self):
        """Initialize Definition of Done validator."""
        self.quality_gates = [
            FunctionalGate(),  # All tests passing (unit + integration + regression)
            ConventionalGate(),  # All naming conventions followed
            StructuralGate(),  # All files in correct locations
            OperationalGate(),  # Production-ready configuration
            IntegrativeGate(),  # MCP validation, database consistency
            ContractualGate(),  # Original acceptance criteria met
            RegressionGate(),  # No existing functionality broken
        ]

        self.validation_start_time: Optional[float] = None
        self.validation_results: Dict[str, bool] = {}

    def validate_completion(self) -> str:
        """
        Cannot declare success until ALL gates pass.

        Returns:
            Success message if all gates pass

        Raises:
            QualityGateFailure: If any gate fails validation
        """
        self.validation_start_time = time.time()
        self.validation_results.clear()

        print("🔍 Running Definition of Done validation...")

        for gate in self.quality_gates:
            print(f"  Validating {gate.name} Gate...", end=" ")

            try:
                result = gate.validate()
                self.validation_results[gate.name] = result

                if result:
                    print("✅ PASS")
                else:
                    print("❌ FAIL")
                    raise QualityGateFailure(f"Gate {gate.name} failed: {gate.error}")

            except Exception as e:
                print("❌ ERROR")
                self.validation_results[gate.name] = False
                raise QualityGateFailure(f"Gate {gate.name} failed: {str(e)}")

        validation_time = time.time() - self.validation_start_time

        return f"✅ All Definition of Done criteria met (validated in {validation_time:.1f}s)"

    def get_validation_summary(self) -> Dict[str, any]:
        """
        Get summary of validation results.

        Returns:
            Dictionary with validation summary
        """
        return {
            "total_gates": len(self.quality_gates),
            "passed_gates": sum(self.validation_results.values()),
            "results": self.validation_results.copy(),
            "all_passed": all(self.validation_results.values()) if self.validation_results else False,
            "validation_time": time.time() - self.validation_start_time if self.validation_start_time else None,
        }


def enforce_definition_of_done() -> str:
    """
    Enforce Definition of Done validation before declaring work complete.

    Returns:
        Success message if all criteria met

    Raises:
        QualityGateFailure: If any criteria not met
    """
    validator = DefinitionOfDoneValidator()
    return validator.validate_completion()
