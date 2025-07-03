"""
Design document compliance checker for enhanced /work command automation.

This module handles DESIGN.md analysis, handoff automation, and implementation
fidelity tracking to ensure work follows the designed technical approach.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Tuple


class DesignCompliance:
    """Handles design document compliance validation and handoff automation."""

    def __init__(self):
        """Initialize the design compliance checker."""
        self.design_requirements: List[str] = []
        self.technical_approach: str = ""
        self.acceptance_criteria: List[Dict[str, str]] = []

    def handle_design_handoff(self, issue_number: int) -> bool:
        """
        Move DESIGN.md from analysis/0000/ to analysis/$ISSUE/.

        Args:
            issue_number: GitHub issue number for the handoff

        Returns:
            True if handoff was successful, False otherwise
        """
        source_path = Path("analysis/0000/DESIGN.md")
        target_dir = Path(f"analysis/{issue_number}")
        target_path = target_dir / "DESIGN.md"

        if not source_path.exists():
            print("⚠️  No DESIGN.md found in analysis/0000/")
            return False

        try:
            # Ensure target directory exists
            target_dir.mkdir(parents=True, exist_ok=True)

            # Move the file
            shutil.move(str(source_path), str(target_path))
            print(f"✅ DESIGN.md moved to analysis/{issue_number}/")
            return True

        except Exception as e:
            print(f"❌ Error moving DESIGN.md: {e}")
            return False

    def load_design_document(self, issue_number: int) -> bool:
        """
        Load and parse design document for compliance tracking.

        Args:
            issue_number: GitHub issue number to load design for

        Returns:
            True if design document was loaded successfully
        """
        design_path = Path(f"analysis/{issue_number}/DESIGN.md")

        if not design_path.exists():
            print(f"⚠️  No DESIGN.md found for issue {issue_number}")
            return False

        try:
            content = design_path.read_text()
            self._parse_design_document(content)
            return True
        except Exception as e:
            print(f"❌ Error loading design document: {e}")
            return False

    def _parse_design_document(self, content: str) -> None:
        """
        Parse design document content to extract requirements.

        Args:
            content: Raw DESIGN.md content
        """
        lines = content.split("\n")
        current_section = ""

        for line in lines:
            line = line.strip()

            # Track sections
            if line.startswith("#"):
                current_section = line.lower()

            # Extract scope requirements (M/S/W items)
            if line.startswith("- **[M]**") or line.startswith("- **[S]**") or line.startswith("- **[W]**"):
                requirement = line.replace("- **[M]**", "").replace("- **[S]**", "").replace("- **[W]**", "").strip()
                self.design_requirements.append(requirement)

            # Extract technical approach from various sections
            if "technical" in current_section and line and not line.startswith("#"):
                self.technical_approach += line + " "

            # Extract acceptance criteria table rows
            if "|" in line and "given" in line.lower():
                parts = [part.strip() for part in line.split("|") if part.strip()]
                if len(parts) >= 4:
                    self.acceptance_criteria.append(
                        {"number": parts[0], "given": parts[1], "when": parts[2], "then": parts[3]}
                    )

    def validate_implementation_approach(self, implementation_summary: str) -> Tuple[bool, List[str]]:
        """
        Validate that implementation follows the designed technical approach.

        Args:
            implementation_summary: Summary of what was implemented

        Returns:
            Tuple of (is_compliant, list_of_deviations)
        """
        deviations = []

        # Check if key technical terms from design are present in implementation
        design_keywords = self._extract_technical_keywords(self.technical_approach)
        impl_keywords = self._extract_technical_keywords(implementation_summary)

        missing_keywords = set(design_keywords) - set(impl_keywords)
        if missing_keywords:
            deviations.append(f"Missing technical components: {', '.join(missing_keywords)}")

        # Check if all design requirements are addressed
        for requirement in self.design_requirements:
            if not self._requirement_addressed_in_implementation(requirement, implementation_summary):
                deviations.append(f"Design requirement not addressed: {requirement}")

        return len(deviations) == 0, deviations

    def check_acceptance_criteria_coverage(self, test_results: Dict[str, bool]) -> Tuple[bool, List[str]]:
        """
        Check if all acceptance criteria are covered by tests.

        Args:
            test_results: Dictionary mapping test names to pass/fail status

        Returns:
            Tuple of (all_covered, list_of_missing_criteria)
        """
        missing_criteria = []

        for criteria in self.acceptance_criteria:
            # Look for tests that match this acceptance criteria
            criteria_covered = any(self._test_covers_criteria(test_name, criteria) for test_name in test_results.keys())

            if not criteria_covered:
                missing_criteria.append(f"Criteria {criteria['number']}: {criteria['given']} -> {criteria['then']}")

        return len(missing_criteria) == 0, missing_criteria

    def generate_compliance_report(self) -> Dict[str, any]:
        """
        Generate a comprehensive compliance report.

        Returns:
            Dictionary containing compliance status and details
        """
        return {
            "design_loaded": len(self.design_requirements) > 0,
            "requirements_count": len(self.design_requirements),
            "acceptance_criteria_count": len(self.acceptance_criteria),
            "technical_approach_defined": len(self.technical_approach.strip()) > 0,
            "requirements": self.design_requirements,
            "acceptance_criteria": self.acceptance_criteria,
        }

    def _extract_technical_keywords(self, text: str) -> List[str]:
        """Extract technical keywords from text."""
        # Simple keyword extraction - in practice this could be more sophisticated
        technical_terms = [
            "python",
            "javascript",
            "neo4j",
            "mcp",
            "snake_case",
            "camelcase",
            "quality gates",
            "validation",
            "automation",
            "convention",
            "testing",
            "database",
            "index",
            "schema",
            "performance",
            "security",
        ]

        text_lower = text.lower()
        found_terms = [term for term in technical_terms if term in text_lower]
        return found_terms

    def _requirement_addressed_in_implementation(self, requirement: str, implementation: str) -> bool:
        """Check if a design requirement is addressed in the implementation."""
        # Simple keyword matching - could be enhanced with NLP
        requirement_words = requirement.lower().split()
        implementation_lower = implementation.lower()

        # At least 50% of requirement words should be present
        matches = sum(1 for word in requirement_words if word in implementation_lower)
        return matches >= len(requirement_words) * 0.5

    def _test_covers_criteria(self, test_name: str, criteria: Dict[str, str]) -> bool:
        """Check if a test covers specific acceptance criteria."""
        test_name_lower = test_name.lower()

        # Check if test name contains keywords from the criteria
        criteria_text = f"{criteria['given']} {criteria['when']} {criteria['then']}".lower()
        criteria_words = criteria_text.split()

        # Simple matching - test name should contain some criteria keywords
        matches = sum(1 for word in criteria_words if word in test_name_lower)
        return matches >= 2  # At least 2 matching words


class DesignDeviationAlert:
    """Handles alerts when implementation deviates from design."""

    def __init__(self):
        """Initialize deviation alert system."""
        self.deviations: List[Dict[str, str]] = []

    def record_deviation(self, deviation_type: str, description: str, suggestion: str) -> None:
        """
        Record a design deviation.

        Args:
            deviation_type: Type of deviation (technical, scope, approach)
            description: Description of the deviation
            suggestion: Suggested action to address deviation
        """
        self.deviations.append(
            {
                "type": deviation_type,
                "description": description,
                "suggestion": suggestion,
                "timestamp": str(Path(".").stat().st_mtime),  # Simple timestamp
            }
        )

    def prompt_user_for_confirmation(self, deviation: Dict[str, str]) -> bool:
        """
        Prompt user to confirm if deviation is acceptable.

        Args:
            deviation: Deviation details

        Returns:
            True if user confirms deviation is acceptable
        """
        print("\n⚠️  Design Deviation Detected:")
        print(f"Type: {deviation['type']}")
        print(f"Description: {deviation['description']}")
        print(f"Suggestion: {deviation['suggestion']}")

        # In a real implementation, this would prompt for user input
        # For testing purposes, we'll return False to indicate deviation not accepted
        return False

    def get_deviation_report(self) -> List[Dict[str, str]]:
        """Get list of all recorded deviations."""
        return self.deviations.copy()
