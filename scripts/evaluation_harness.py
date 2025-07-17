"""Evaluation Test Harness v2.

Git-native 5-state workflow with automated progress tracking for evaluation tests.
Implements the architecture defined in analysis/0000/DESIGN.md.
"""

import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class TestState(Enum):
    """Test states in the evaluation harness."""

    TODO = "TODO"
    REVIEW = "REVIEW"
    PASSED = "PASSED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass
class TestResult:
    """Result of running an evaluation test."""

    passed: bool
    duration_ms: int
    confidence: Optional[float] = None
    expected_count: Optional[int] = None
    actual_count: Optional[int] = None
    expected_score: Optional[float] = None
    actual_score: Optional[float] = None
    error: Optional[str] = None
    output: Optional[str] = None


@dataclass
class TestFile:
    """Represents an evaluation test file with metadata."""

    id: str
    status: TestState
    category: str
    added: str
    last_run: Optional[str] = None
    duration_ms: Optional[int] = None
    run_count: int = 0
    blocker: str = "—"
    path: Optional[Path] = None
    content: str = ""

    @classmethod
    def from_path(cls, file_path: Path) -> "TestFile":
        """Parse test file from filesystem path."""
        if not file_path.exists():
            raise FileNotFoundError(f"Test file not found: {file_path}")

        content = file_path.read_text()

        # Parse machine-readable header
        # Look for the header pattern and capture everything until the first markdown header
        lines = content.split("\n")
        # Be more flexible with the META comment format
        if not (lines[0].startswith("<!--- META:") or lines[0].startswith("<!--META:") or "META:" in lines[0]):
            raise ValueError(f"Invalid test file format: {file_path} - first line: {lines[0]!r}")

        # Find where the metadata ends (blank line or markdown header)
        meta_lines = []
        for i, line in enumerate(lines[1:], 1):
            if line.startswith("#") or (line.strip() == "" and i < len(lines) - 1 and lines[i + 1].startswith("#")):
                break
            if line.strip():  # Only include non-empty lines
                meta_lines.append(line)

        # Parse metadata from lines
        metadata = {}
        for line in meta_lines:
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        # Validate we have required fields
        if not metadata.get("ID"):
            raise ValueError(f"Invalid test file format: {file_path} - missing ID field. Metadata: {metadata}")

        return cls(
            id=metadata.get("ID", ""),
            status=TestState(metadata.get("Status", "TODO")),
            category=metadata.get("Category", ""),
            added=metadata.get("Added", ""),
            last_run=metadata.get("Last-Run") if metadata.get("Last-Run") != "—" else None,
            duration_ms=int(metadata.get("Duration-ms")) if metadata.get("Duration-ms", "—").isdigit() else None,
            run_count=int(metadata.get("Run-Count", "0")),
            blocker=metadata.get("Blocker", "—"),
            path=file_path,
            content=content,
        )

    def update_header(self, **kwargs) -> str:
        """Update the machine-readable header with new values."""
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Generate updated header
        header = f"""<!--- META: machine-readable for scripts --->
Status: {self.status.value}
ID: {self.id}
Category: {self.category}
Added: {self.added}
Last-Run: {self.last_run or "—"}
Duration-ms: {self.duration_ms or "—"}
Run-Count: {self.run_count}
Blocker: {self.blocker}

"""

        # Replace header in content - find everything from the comment to the first markdown header
        lines = self.content.split("\n")

        # Find where the old header ends (first markdown header starting with #)
        header_end = len(lines)
        for i, line in enumerate(lines[1:], 1):
            if line.startswith("#"):
                header_end = i
                break

        # Reconstruct content with new header + original content after header
        remaining_content = "\n".join(lines[header_end:])
        updated_content = header + remaining_content

        return updated_content


class EvaluationHarness:
    """Main evaluation harness for managing test lifecycle."""

    def __init__(self, evals_dir: Path):
        """Initialize evaluation harness."""
        self.evals_dir = Path(evals_dir)
        self.folders = ["todo", "review", "passed", "failed", "blocked"]

    def create_folder_structure(self):
        """Create the 5-folder structure and template."""
        self.evals_dir.mkdir(parents=True, exist_ok=True)

        # Create state folders
        for folder in self.folders:
            (self.evals_dir / folder).mkdir(exist_ok=True)

        # Create template.md
        template_content = """<!--- META: machine-readable for scripts --->
Status: TODO
ID: EVAL-XX
Category: <one-word tag>
Added: {date}
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

# EVAL-XX: [Question/Title]

## Question
[The evaluation question or prompt]

## Expected Answer
[What the correct response should be]

## Implementation

### Query
```cypher
// Cypher query or implementation approach
```

### Actual Result
```
[Results when executed]
```

## Validation
[Pass/fail status and notes]

## Technical Implementation
[Technical details about search categories, etc.]

## Business Value
[Why this test matters for law enforcement use cases]
""".format(date=datetime.now().strftime("%Y-%m-%d"))

        (self.evals_dir / "template.md").write_text(template_content)

    def calculate_confidence(
        self, expected_count: int, actual_count: int, expected_score: float, actual_score: float
    ) -> float:
        """Calculate confidence score for auto-promotion.

        Returns confidence percentage (0-100) based on:
        - Count accuracy (70% weight): How well actual count matches expected
        - Score similarity (30% weight): How close scores are to expected

        Auto-promotion threshold: 80%
        """
        if expected_count <= 0 or expected_score <= 0:
            return 0.0

        # Count accuracy: how well actual matches expected
        count_accuracy = min(actual_count, expected_count) / expected_count

        # Score similarity: inverse of relative difference
        score_diff = abs(actual_score - expected_score) / expected_score
        score_similarity = max(0, 1 - score_diff)

        # Weighted confidence calculation
        confidence = (count_accuracy * 0.7) + (score_similarity * 0.3)

        return confidence * 100  # Return as percentage

    def transition_test(self, test_id: str, from_state: TestState, to_state: TestState):
        """Transition a test between states using git mv."""
        from_folder = from_state.value.lower()
        to_folder = to_state.value.lower()

        from_path = self.evals_dir / from_folder / f"{test_id}.md"
        to_path = self.evals_dir / to_folder / f"{test_id}.md"

        if not from_path.exists():
            raise FileNotFoundError(f"Test file not found: {from_path}")

        # Ensure target folder exists
        to_path.parent.mkdir(exist_ok=True)

        try:
            # Try git mv first (preferred for version control)
            subprocess.run(
                ["git", "mv", str(from_path), str(to_path)], cwd=self.evals_dir.parent, check=True, capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to regular file move (for testing/non-git environments)
            shutil.move(str(from_path), str(to_path))

    def run_test(self, test_id: str) -> TestResult:
        """Execute a test and return results."""
        # Find test file in any folder
        test_file = None
        original_path = None
        for folder in self.folders:
            test_path = self.evals_dir / folder / f"{test_id}.md"
            if test_path.exists():
                test_file = TestFile.from_path(test_path)
                original_path = test_path
                break

        if not test_file:
            return TestResult(passed=False, duration_ms=0, error=f"Test {test_id} not found")

        # Simulate test execution (simplified for MVP)
        start_time = time.time()

        try:
            # Extract expected results from test file
            expected_count = None
            expected_score = None
            actual_count = None
            actual_score = None
            confidence = None

            # Look for expected results in the confidence calculation section
            expected_match = re.search(r"Expected:\s*\[count:\s*(\d+),\s*score:\s*([\d.]+)\]", test_file.content)
            if expected_match:
                expected_count = int(expected_match.group(1))
                expected_score = float(expected_match.group(2))

            # Look for actual results in the confidence calculation section
            actual_match = re.search(r"Actual:\s*\[count:\s*(\d+),\s*score:\s*([\d.]+)\]", test_file.content)
            if actual_match:
                actual_count = int(actual_match.group(1))
                actual_score = float(actual_match.group(2))

            # Calculate confidence if we have expected and actual values
            if all(x is not None for x in [expected_count, expected_score, actual_count, actual_score]):
                confidence = self.calculate_confidence(expected_count, actual_count, expected_score, actual_score)
                passed = confidence >= 80.0  # Auto-promotion threshold
            else:
                # Fallback to simple test detection for backward compatibility
                query_match = re.search(r"```cypher\n(.*?)\n```", test_file.content, re.DOTALL)
                if query_match:
                    query = query_match.group(1).strip()
                    passed = "RETURN 1" in query or "test" in query.lower()
                else:
                    content_lower = test_file.content.lower()
                    passed = "return 1 as test" in content_lower or "query: return 1" in content_lower

            duration_ms = int((time.time() - start_time) * 1000)

            # Update test file header
            test_file.run_count += 1
            test_file.last_run = datetime.now().isoformat()
            test_file.duration_ms = duration_ms

            # Determine new status based on confidence and current state
            if test_file.status == TestState.REVIEW and confidence is not None and confidence >= 80.0:
                new_status = TestState.PASSED  # Auto-promotion
            elif passed and test_file.status == TestState.TODO:
                new_status = TestState.REVIEW  # Move to review for manual verification
            elif not passed:
                new_status = TestState.FAILED
            else:
                new_status = test_file.status  # No change

            # Update file content and move if needed
            if test_file.status != new_status:
                # Capture old status before updating
                old_status = test_file.status

                # Update content with new status
                updated_content = test_file.update_header(status=new_status)

                # Move file to appropriate folder
                self.transition_test(test_id, old_status, new_status)

                # Write updated content to new location
                new_path = self.evals_dir / new_status.value.lower() / f"{test_id}.md"
                new_path.write_text(updated_content)
            else:
                # Just update the header in place
                updated_content = test_file.update_header()
                original_path.write_text(updated_content)

            return TestResult(
                passed=passed,
                duration_ms=duration_ms,
                confidence=confidence,
                expected_count=expected_count,
                actual_count=actual_count,
                expected_score=expected_score,
                actual_score=actual_score,
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return TestResult(passed=False, duration_ms=duration_ms, error=str(e))


class ProgressDashboard:
    """Generate progress dashboard and reports."""

    def __init__(self, evals_dir: Path):
        """Initialize dashboard generator."""
        self.evals_dir = Path(evals_dir)
        self.status_symbols = {
            TestState.TODO: "⬜",
            TestState.REVIEW: "🟠",
            TestState.PASSED: "✅",
            TestState.FAILED: "❌",
            TestState.BLOCKED: "⏸",
        }

    def get_all_tests(self) -> list[TestFile]:
        """Get all test files from all folders."""
        tests = []
        folders = ["todo", "review", "passed", "failed", "blocked"]

        for folder in folders:
            folder_path = self.evals_dir / folder
            if folder_path.exists():
                for file_path in folder_path.glob("EVAL-*.md"):
                    try:
                        test_file = TestFile.from_path(file_path)
                        tests.append(test_file)
                    except Exception as e:
                        print(f"Warning: Could not parse {file_path}: {e}")

        # Sort by ID
        tests.sort(key=lambda t: t.id)
        return tests

    def generate(self) -> str:
        """Generate progress dashboard in markdown format."""
        tests = self.get_all_tests()

        # Generate header
        content = f"""# Evaluation Progress Dashboard

**Last Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Tests**: {len(tests)}

## Status Summary

"""

        # Count by status
        status_counts = {}
        for test in tests:
            status_counts[test.status] = status_counts.get(test.status, 0) + 1

        for status in TestState:
            count = status_counts.get(status, 0)
            symbol = self.status_symbols[status]
            content += f"- {symbol} **{status.value}**: {count}\n"

        content += "\n## Test Details\n\n"
        content += "| ID | Question | Status | Last Run | Duration | Notes |\n"
        content += "|----|---------|---------|-----------|-----------|---------|\n"

        for test in tests:
            symbol = self.status_symbols[test.status]
            last_run = test.last_run.split("T")[0] if test.last_run else "—"
            duration = f"{test.duration_ms} ms" if test.duration_ms else "—"
            notes = test.blocker if test.blocker != "—" else "—"

            # Extract question from content
            title_match = re.search(r"^# EVAL-\d+:\s*(.+)$", test.content, re.MULTILINE)
            question = title_match.group(1) if title_match else "—"

            content += f"| {test.id} | {question} | {symbol} | {last_run} | {duration} | {notes} |\n"

        content += "\n## Legend\n"
        for status in TestState:
            symbol = self.status_symbols[status]
            content += f"- {symbol} {status.value.title()}\n"

        return content

    def export_csv(self) -> str:
        """Export test status to CSV format."""
        tests = self.get_all_tests()

        lines = ["ID,Question,Status,Last Run,Duration,Notes"]

        for test in tests:
            last_run = test.last_run.split("T")[0] if test.last_run else ""
            duration = str(test.duration_ms) if test.duration_ms else ""
            notes = test.blocker if test.blocker != "—" else ""

            # Extract question from content
            title_match = re.search(r"^# EVAL-\d+:\s*(.+)$", test.content, re.MULTILINE)
            question = title_match.group(1) if title_match else ""

            # Escape commas in question
            question = question.replace(",", ";")

            lines.append(f"{test.id},{question},{test.status.value},{last_run},{duration},{notes}")

        return "\n".join(lines)


def migrate_existing_tests(evals_dir: Path):
    """Migrate existing tests from implemented/pending to new structure."""
    # Create new structure
    harness = EvaluationHarness(evals_dir)
    harness.create_folder_structure()

    # Load the master evaluation table to understand all 77 tests
    evaluation_table = _load_evaluation_table(evals_dir.parent / "evals" / "evaluation_tests.md")

    # Track which evaluations we've migrated
    migrated_evaluations = set()

    # Migrate implemented tests to review folder
    implemented_dir = evals_dir / "implemented"
    if implemented_dir.exists():
        for file_path in implemented_dir.glob("*.md"):
            # Add header to existing file
            content = file_path.read_text()

            # Extract EVAL-XX from filename
            eval_id = file_path.stem
            migrated_evaluations.add(eval_id)

            # Get category and prompt from master table
            eval_data = evaluation_table.get(eval_id, {})
            category = _categorize_evaluation(eval_data.get("category", ""), content)

            # Prepend header
            header = f"""<!--- META: machine-readable for scripts --->
Status: REVIEW
ID: {eval_id}
Category: {category}
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

"""
            updated_content = header + content

            # Write to review folder
            review_file = evals_dir / "review" / file_path.name
            review_file.write_text(updated_content)

            # Remove from old location
            file_path.unlink()

    # Migrate pending tests to todo folder
    pending_dir = evals_dir / "pending"
    if pending_dir.exists():
        for file_path in pending_dir.glob("*.md"):
            content = file_path.read_text()
            eval_id = file_path.stem
            migrated_evaluations.add(eval_id)

            # Get category and prompt from master table
            eval_data = evaluation_table.get(eval_id, {})
            category = _categorize_evaluation(eval_data.get("category", ""), content)

            header = f"""<!--- META: machine-readable for scripts --->
Status: TODO
ID: {eval_id}
Category: {category}
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: —

"""
            updated_content = header + content

            # Write to todo folder
            todo_file = evals_dir / "todo" / file_path.name
            todo_file.write_text(updated_content)

            # Remove from old location
            file_path.unlink()

    # Create missing evaluation files for the remaining tests (from 77 total)
    for eval_id, eval_data in evaluation_table.items():
        if eval_id not in migrated_evaluations:
            _create_evaluation_stub(evals_dir, eval_id, eval_data)

    # Remove old folders if empty
    if implemented_dir.exists() and not any(implemented_dir.iterdir()):
        implemented_dir.rmdir()
    if pending_dir.exists() and not any(pending_dir.iterdir()):
        pending_dir.rmdir()


def _load_evaluation_table(evaluation_tests_path: Path) -> dict[str, dict[str, str]]:
    """Load the 77 evaluation tests from evaluation_tests.md."""
    if not evaluation_tests_path.exists():
        return {}

    content = evaluation_tests_path.read_text()

    # Parse the table (simplified - assumes standard markdown table format)
    evaluations = {}
    lines = content.split("\n")

    # Find the table start (after "| # | Theme | Prompt |")
    table_start = -1
    for i, line in enumerate(lines):
        if line.startswith("| # | Theme | Prompt |"):
            table_start = i + 2  # Skip header and separator
            break

    if table_start == -1:
        return evaluations

    # Parse table rows
    for line in lines[table_start:]:
        if not line.strip() or not line.startswith("|"):
            continue

        parts = [part.strip() for part in line.split("|")[1:-1]]  # Remove empty first/last
        if len(parts) >= 4:
            try:
                eval_num = int(parts[0])
                eval_id = f"EVAL-{eval_num:02d}"
                evaluations[eval_id] = {
                    "theme": parts[1],
                    "prompt": parts[2],
                    "expected": parts[3],
                    "category": parts[4] if len(parts) > 4 else "Communications",
                }
            except ValueError:
                continue

    return evaluations


def _categorize_evaluation(category_text: str, content: str = "") -> str:
    """Determine category from evaluation metadata."""
    category_lower = category_text.lower()
    content_lower = content.lower()

    if "semantic" in category_lower or "search" in category_lower:
        return "Search"
    elif "metadata" in category_lower or "filter" in category_lower:
        return "Metadata"
    elif "translation" in category_lower:
        return "Translation"
    elif "alignment" in category_lower:
        return "Alignment"
    elif "knowledge" in category_lower:
        return "Knowledge"
    elif "network" in content_lower or "traversal" in category_lower:
        return "Network"
    elif "analytic" in content_lower:
        return "Analytics"
    else:
        return "Communications"  # Default


def _create_evaluation_stub(evals_dir: Path, eval_id: str, eval_data: dict[str, str]):
    """Create a stub evaluation file for missing tests."""
    category = _categorize_evaluation(eval_data.get("category", ""))
    prompt = eval_data.get("prompt", "")
    expected = eval_data.get("expected", "")
    theme = eval_data.get("theme", "Communications")

    # Determine initial status based on complexity
    if "alignment" in category.lower() or "translation" in category.lower() or "knowledge" in category.lower():
        status = "BLOCKED"
        blocker = "Framework feature - not core Neo4j functionality"
        folder = "blocked"
    else:
        status = "TODO"
        blocker = "—"
        folder = "todo"

    # Create stub content
    content = f"""<!--- META: machine-readable for scripts --->
Status: {status}
ID: {eval_id}
Category: {category}
Added: 2025-07-03
Last-Run: —
Duration-ms: —
Run-Count: 0
Blocker: {blocker}

# {eval_id}: {theme}

## Question
{prompt}

## Expected Answer
{expected}

## Implementation

### Query
```cypher
// TODO: Implement Cypher query
```

### Actual Result
```
// TODO: Execute and record results
```

## Validation
**Status**: ⏳ **NOT YET IMPLEMENTED**

## Technical Implementation

### Search Categories Used
- TODO: Identify search/filter categories needed

## Business Value

This evaluation tests the system's ability to handle {theme.lower()} scenarios for law enforcement investigations.
"""

    # Write to appropriate folder
    file_path = evals_dir / folder / f"{eval_id}.md"
    file_path.write_text(content)


def run_evaluation_test(test_id: str, evals_dir: Optional[Path] = None) -> TestResult:
    """Run a single evaluation test by ID."""
    if evals_dir is None:
        evals_dir = Path("evals")

    harness = EvaluationHarness(evals_dir)
    return harness.run_test(test_id)


def main():
    """Main entry point for evaluation harness."""
    import argparse

    parser = argparse.ArgumentParser(description="Evaluation Test Harness v2")
    parser.add_argument("command", choices=["migrate", "run", "dashboard", "csv"], help="Command to execute")
    parser.add_argument("--test-id", help="Test ID for run command")
    parser.add_argument("--evals-dir", default="evals", help="Evaluations directory")

    args = parser.parse_args()

    evals_dir = Path(args.evals_dir)

    if args.command == "migrate":
        print("Migrating existing tests...")
        migrate_existing_tests(evals_dir)
        print("Migration complete!")

    elif args.command == "run":
        if not args.test_id:
            print("Error: --test-id required for run command")
            return

        harness = EvaluationHarness(evals_dir)
        result = harness.run_test(args.test_id)

        print(f"Test {args.test_id}: {'PASSED' if result.passed else 'FAILED'}")
        print(f"Duration: {result.duration_ms}ms")
        if result.error:
            print(f"Error: {result.error}")

    elif args.command == "dashboard":
        dashboard = ProgressDashboard(evals_dir)
        content = dashboard.generate()

        # Write to progress.md
        (evals_dir / "progress.md").write_text(content)
        print("Progress dashboard updated!")

    elif args.command == "csv":
        dashboard = ProgressDashboard(evals_dir)
        csv_content = dashboard.export_csv()

        # Write to progress.csv
        (evals_dir / "progress.csv").write_text(csv_content)
        print("CSV export complete!")


if __name__ == "__main__":
    main()
