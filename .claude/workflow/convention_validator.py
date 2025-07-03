"""
Minimal convention validator for basic code quality checks.

This module provides simple, language-agnostic validation following the
"less is more" principle. Let Claude handle language-specific conventions naturally.
"""

import os
import shutil
from pathlib import Path
from typing import List


class ConventionValidator:
    """Minimal validator for basic project conventions."""

    def __init__(self):
        """Initialize the convention validator."""
        self.project_type = self._detect_project_type()

    def _detect_project_type(self) -> str:
        """Detect project type based on configuration files."""
        if Path("pyproject.toml").exists() or Path("requirements.txt").exists():
            return "python"
        elif Path("package.json").exists():
            return "javascript"
        else:
            return "mixed"

    def detect_project_type(self) -> str:
        """Public method to get project type."""
        return self.project_type

    @property
    def naming_convention(self) -> str:
        """Get the expected naming convention for this project type."""
        if self.project_type == "python":
            return "snake_case"
        elif self.project_type == "javascript":
            return "camelCase"
        else:
            return "mixed"

    @property
    def test_directory(self) -> str:
        """Get the expected test directory for this project type."""
        if self.project_type == "python":
            return "./tests/"
        elif self.project_type == "javascript":
            return "./__tests__/"
        else:
            return "./tests/"

    def validate_naming(self, file_path: str, content: str) -> List[dict]:
        """
        Minimal naming validation.

        Args:
            file_path: Path to the file being validated
            content: File content to validate

        Returns:
            List of violations (kept minimal)
        """
        # Let Claude handle language-specific conventions naturally
        return []

    def check_snake_case_violations(self, content: str) -> List[dict]:
        """
        Minimal check for obvious naming issues in Python.
        Let Claude handle detailed convention review naturally.

        Args:
            content: Code content to check

        Returns:
            List of obvious violations only
        """
        # Keep it minimal - just return empty list
        # Claude will naturally enforce conventions when reviewing code
        return []

    def check_camel_case_violations(self, content: str) -> List[dict]:
        """Check for camelCase violations - kept minimal."""
        return []

    def validate_file_placement(self, file_path: str) -> bool:
        """
        Validate that files are in correct locations.

        Args:
            file_path: Path to the file to validate

        Returns:
            True if file is in correct location, False otherwise
        """
        return not self.should_move_test_file(file_path)

    def should_move_test_file(self, file_path: str) -> bool:
        """
        Check if a test file should be moved to the correct directory.

        Args:
            file_path: Path to the test file

        Returns:
            True if file should be moved, False otherwise
        """
        if self.project_type == "python":
            # Python test files should be in ./tests/
            if file_path.startswith("test_") or file_path.endswith("_test.py"):
                return not file_path.startswith("tests/")
        elif self.project_type == "javascript":
            # JavaScript test files should be in ./__tests__/
            if file_path.endswith(".test.js") or file_path.endswith(".spec.js"):
                return not file_path.startswith("__tests__/")

        return False

    def get_correct_test_location(self, file_path: str) -> str:
        """
        Get the correct location for a test file.

        Args:
            file_path: Current path of the test file

        Returns:
            Correct path for the test file
        """
        filename = os.path.basename(file_path)

        if self.project_type == "python":
            return f"tests/{filename}"
        elif self.project_type == "javascript":
            return f"__tests__/{filename}"
        else:
            return f"tests/{filename}"

    def auto_move_file(self, source_path: str, target_path: str) -> bool:
        """
        Automatically move a file to the correct location.

        Args:
            source_path: Current file path
            target_path: Target file path

        Returns:
            True if move was successful, False otherwise
        """
        try:
            # Ensure target directory exists
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)

            # Move the file
            shutil.move(source_path, target_path)
            return True
        except Exception as e:
            print(f"Error moving file {source_path} to {target_path}: {e}")
            return False

    def auto_fix_or_fail(self, violations: List[dict]) -> None:
        """
        Attempt to auto-fix violations or raise an error.

        Args:
            violations: List of naming convention violations

        Raises:
            ConventionViolationError: If violations cannot be auto-fixed
        """
        if violations:
            violation_messages = []
            for violation in violations:
                violation_messages.append(f"Line {violation['line']}: {violation['issue']}. {violation['suggestion']}")

            raise ConventionViolationError("Convention violations detected:\n" + "\n".join(violation_messages))


class ConventionViolationError(Exception):
    """Exception raised when convention violations are detected."""

    pass
