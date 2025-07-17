"""
Neo4j Query Executor - Interactive Development + Automated Confidence Processing

Part 1: Interactive query development using proven "dance" methodology
Part 2: Automated confidence processing for batch operations

This implementation follows evaluation-first development:
- All functionality tested before implementation
- Simple, focused solution following "nothing left to take away" principle
- Integration with existing evaluation harness system
"""

import glob
import re
from pathlib import Path
from typing import Any, Optional


def find_evaluation_test(test_id: str, evals_dir: Path) -> Path:
    """
    Find evaluation test file by ID across all folders.

    Args:
        test_id: Test ID like "05", "42", or "EVAL-05"
        evals_dir: Path to evals directory

    Returns:
        Path to the test file

    Raises:
        ValueError: If multiple files found or no files found
    """
    # Normalize test ID - handle both "05" and "EVAL-05" formats
    if test_id.startswith("EVAL-"):
        clean_id = test_id[5:]  # Remove "EVAL-" prefix
    else:
        clean_id = test_id

    # Ensure 2-digit format
    clean_id = clean_id.zfill(2)

    # Search across all folders
    pattern = str(evals_dir / "*" / f"EVAL-{clean_id}.md")
    matching_files = glob.glob(pattern)

    if len(matching_files) == 0:
        raise ValueError(f"No test file found for EVAL-{clean_id}. Valid range: 01-77")

    if len(matching_files) > 1:
        file_paths = [Path(f).relative_to(evals_dir) for f in matching_files]
        raise ValueError(f"Multiple test files found for EVAL-{clean_id}: {file_paths}")

    return Path(matching_files[0])


def load_business_context(test_id: str, evals_dir: Path) -> dict[str, str]:
    """
    Load business context from evaluation_tests.md table.

    Args:
        test_id: Test ID like "05" or "42"
        evals_dir: Path to evals directory

    Returns:
        Dictionary with theme, prompt, expected_response, and search_category
    """
    # Normalize test ID
    if test_id.startswith("EVAL-"):
        clean_id = test_id[5:]
    else:
        clean_id = test_id

    clean_id = clean_id.zfill(2)
    eval_id = f"EVAL-{clean_id}"

    # Read evaluation_tests.md
    eval_tests_file = evals_dir / "evaluation_tests.md"
    if not eval_tests_file.exists():
        return {
            "theme": "Unknown",
            "prompt": "Business context not available",
            "expected_response": "See test file",
            "search_category": "General",
        }

    content = eval_tests_file.read_text()

    # Parse table - look for line starting with eval_id
    for line in content.split("\n"):
        if line.strip().startswith(f"| {eval_id}"):
            # Split by | and clean up
            parts = [part.strip() for part in line.split("|")]
            if len(parts) >= 6:  # | EVAL-NN | Theme | Prompt | Expected | Category |
                return {
                    "theme": parts[2],
                    "prompt": parts[3],
                    "expected_response": parts[4],
                    "search_category": parts[5],
                }

    # If not found in table, return defaults
    return {
        "theme": "Unknown",
        "prompt": "Business context not available - check evaluation_tests.md",
        "expected_response": "See test file for requirements",
        "search_category": "General",
    }


class EvalCommand:
    """
    Interactive evaluation test development command.

    Implements the /eval NN workflow for developing Cypher queries
    with immediate Neo4j MCP feedback and confidence assessment.
    """

    def __init__(self, project_dir: Path):
        """Initialize command with project directory."""
        self.project_dir = Path(project_dir)
        self.evals_dir = self.project_dir / "evals"

    def run(self, test_id: str) -> dict[str, Any]:
        """
        Run interactive evaluation test development.

        Args:
            test_id: Test ID like "05", "42", or "EVAL-05"

        Returns:
            Dictionary with results of the development session
        """
        # Find test file
        try:
            test_file = find_evaluation_test(test_id, self.evals_dir)
        except ValueError as e:
            return {"error": str(e)}

        # Load business context
        context = load_business_context(test_id, self.evals_dir)

        # Read current test file
        current_content = test_file.read_text()

        # Check if already has non-placeholder query
        if "// TODO: Implement Cypher query" not in current_content:
            return {
                "status": "has_query",
                "message": f"Test {test_id} already has a query. Use improvement workflow.",
                "file_path": test_file,
                "context": context,
            }

        # Run interactive development
        development_result = self.interactive_query_development(test_id, context)

        # Update test file with results
        self.update_test_file(
            test_file, development_result["query"], development_result["confidence"], development_result["assessment"]
        )

        return {
            "status": "completed",
            "file_path": test_file,
            "context": context,
            "query": development_result["query"],
            "confidence": development_result["confidence"],
        }

    def interactive_query_development(self, test_id: str, context: dict[str, str]) -> dict[str, Any]:
        """
        Placeholder for interactive query development using MCP.

        In real implementation, this would:
        1. Use mcp__neo4j__get_neo4j_schema() to explore database
        2. Use mcp__neo4j__read_neo4j_cypher() to test queries
        3. Iterate until query correctly answers business question
        4. Get human assessment (Y/Partial/N)
        5. Return final query and confidence

        Args:
            test_id: Test ID being developed
            context: Business context from evaluation_tests.md

        Returns:
            Dictionary with query, confidence, and assessment
        """
        # This would be implemented with actual MCP calls
        # For testing, return mock structure
        return {"query": "MATCH (p:Person) WHERE p.name = 'John' RETURN p", "confidence": 80, "assessment": "Y"}

    def update_test_file(self, test_file: Path, query: str, confidence: int, assessment: str) -> bool:
        """
        Update test file with developed query and confidence section.

        Args:
            test_file: Path to test file
            query: Developed Cypher query
            confidence: Confidence percentage (30, 70, or 80)
            assessment: Human assessment (Y, Partial, N)

        Returns:
            True if update successful
        """
        current_content = test_file.read_text()

        # Replace placeholder query
        updated_content = current_content.replace("// TODO: Implement Cypher query", query)

        # Add confidence section
        confidence_section = self._generate_confidence_section(confidence, assessment)

        # Insert confidence section before "## Technical Implementation" if it exists
        if "## Technical Implementation" in updated_content:
            updated_content = updated_content.replace(
                "## Technical Implementation", f"{confidence_section}\n\n## Technical Implementation"
            )
        else:
            # Append to end
            updated_content += f"\n\n{confidence_section}"

        # Write back to file
        test_file.write_text(updated_content)
        return True

    def _generate_confidence_section(self, confidence: int, assessment: str) -> str:
        """Generate confidence section with new simple format."""
        action_map = {80: "Auto-promote to PASSED", 70: "Stay in REVIEW", 30: "Auto-fail to FAILED"}

        assessment_map = {"Y": "✅ **Correct**", "Partial": "⚠️ **Partially Correct**", "N": "❌ **Incorrect**"}

        action = action_map.get(confidence, "Manual review required")
        assessment_text = assessment_map.get(assessment, "Unknown assessment")

        return f"""## Confidence Assessment

**Assessment**: {assessment_text}
**Confidence**: {confidence}% → {action}"""


class ConfidenceProcessor:
    """
    Automated confidence processor for batch operations.

    Processes test files with existing confidence sections and
    auto-promotes/fails based on confidence thresholds.
    """

    def __init__(self, evals_dir: Path):
        """Initialize processor with evals directory."""
        self.evals_dir = Path(evals_dir)

    def parse_confidence_section(self, test_file: Path) -> Optional[dict[str, Any]]:
        """
        Parse confidence section from test file.

        Only recognizes new simple format, ignores legacy calculations.

        Args:
            test_file: Path to test file

        Returns:
            Dictionary with percentage and action, or None if not found
        """
        if not test_file.exists():
            return None

        content = test_file.read_text()

        # Look for new simple format patterns
        patterns = [
            r"\*\*Confidence\*\*:\s*(\d+)%\s*→\s*(Auto-promote to PASSED)",
            r"\*\*Confidence\*\*:\s*(\d+)%\s*→\s*(Auto-fail to FAILED)",
            r"\*\*Confidence\*\*:\s*(\d+)%\s*→\s*(Stay in REVIEW)",
            # Also match simple percentage format
            r"\*\*Confidence\*\*:\s*(\d+)%",
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                percentage = int(match.group(1))
                action = match.group(2) if len(match.groups()) > 1 else "Manual review"
                return {"percentage": percentage, "action": action}

        # Ignore legacy format - return None
        return None

    def process_existing_confidence(self, test_id: Optional[str] = None, batch: bool = False) -> dict[str, int]:
        """
        Process tests with existing confidence sections for auto-promotion.

        Args:
            test_id: Specific test ID to process, or None for all
            batch: Process all eligible tests

        Returns:
            Dictionary with counts of promoted, failed, and skipped tests
        """
        # Find test files
        if test_id:
            # Convert test ID to file pattern
            clean_id = test_id.replace("EVAL-", "").zfill(2)
            test_files = glob.glob(str(self.evals_dir / "*" / f"EVAL-{clean_id}.md"))
        else:
            # All test files
            test_files = glob.glob(str(self.evals_dir / "*" / "EVAL-*.md"))

        promoted_count = 0
        failed_count = 0
        skipped_count = 0

        for test_file_path in test_files:
            test_file = Path(test_file_path)

            # Parse confidence section
            confidence_data = self.parse_confidence_section(test_file)

            if confidence_data is None:
                skipped_count += 1
                continue

            percentage = confidence_data["percentage"]

            # Extract test ID from filename for transition
            filename = test_file.name
            file_test_id = filename.replace(".md", "")

            # Determine current folder from file path
            current_folder = test_file.parent.name.upper()

            # Apply auto-promotion rules
            if percentage >= 80:
                # Auto-promote to PASSED
                self.transition_test(file_test_id, current_folder, "PASSED")
                promoted_count += 1
                print(f"Auto-promoted {file_test_id} with {percentage}% confidence")
            elif percentage <= 30:
                # Auto-fail to FAILED
                self.transition_test(file_test_id, current_folder, "FAILED")
                failed_count += 1
                print(f"Auto-failed {file_test_id} with {percentage}% confidence")
            else:
                # 31-79% stays in current location (no transition)
                skipped_count += 1
                print(f"Skipped {file_test_id} with {percentage}% confidence (stays in current location)")

        return {"promoted_count": promoted_count, "failed_count": failed_count, "skipped_count": skipped_count}

    def transition_test(self, test_id: str, from_state: str, to_state: str) -> bool:
        """
        Transition test file between states using git mv and update metadata.

        Args:
            test_id: Test ID like "EVAL-05"
            from_state: Current state folder name
            to_state: Target state folder name

        Returns:
            True if transition successful
        """
        # Import and use the real evaluation harness
        from scripts.evaluation_harness import EvaluationHarness, TestFile, TestState

        # Map string states to TestState enum
        state_map = {
            "TODO": TestState.TODO,
            "REVIEW": TestState.REVIEW,
            "PASSED": TestState.PASSED,
            "FAILED": TestState.FAILED,
            "BLOCKED": TestState.BLOCKED,
        }

        from_enum = state_map.get(from_state.upper())
        to_enum = state_map.get(to_state.upper())

        if not from_enum or not to_enum:
            print(f"Invalid state: {from_state} → {to_state}")
            return False

        # Use real harness for actual file movement
        harness = EvaluationHarness(self.evals_dir)

        try:
            # Move the file
            harness.transition_test(test_id, from_enum, to_enum)

            # Update the metadata header in the moved file
            new_file_path = self.evals_dir / to_state.lower() / f"{test_id}.md"
            if new_file_path.exists():
                test_file = TestFile.from_path(new_file_path)
                updated_content = test_file.update_header(status=to_enum)
                new_file_path.write_text(updated_content)

            print(f"✅ Moved {test_id}: {from_state} → {to_state}")
            return True
        except Exception as e:
            print(f"❌ Failed to move {test_id}: {e}")
            return False


# CLI interface functions for command-line usage
def main():
    """Main CLI entry point for neo4j_query_executor."""
    import argparse

    parser = argparse.ArgumentParser(description="Neo4j Query Executor")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Eval command
    eval_parser = subparsers.add_parser("eval", help="Interactive evaluation test development")
    eval_parser.add_argument("test_id", help="Test ID (e.g., 05, EVAL-42)")
    eval_parser.add_argument("--project-dir", default=".", help="Project directory path")

    # Confidence processor
    confidence_parser = subparsers.add_parser("confidence", help="Process existing confidence sections")
    confidence_parser.add_argument("--test-id", help="Specific test ID to process")
    confidence_parser.add_argument("--batch", action="store_true", help="Process all eligible tests")
    confidence_parser.add_argument("--evals-dir", default="evals", help="Evaluations directory")

    args = parser.parse_args()

    if args.command == "eval":
        # Interactive eval command
        eval_cmd = EvalCommand(Path(args.project_dir))
        result = eval_cmd.run(args.test_id)
        print(f"Eval command result: {result}")

    elif args.command == "confidence":
        # Confidence processor
        processor = ConfidenceProcessor(Path(args.evals_dir))
        results = processor.process_existing_confidence(test_id=args.test_id, batch=args.batch)
        print(f"Confidence processing results: {results}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
