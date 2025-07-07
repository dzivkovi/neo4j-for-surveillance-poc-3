#!/usr/bin/env python3
"""
Update test counts across all documentation files.

Single source of truth for test statistics.
Run this after any changes to keep documentation in sync.
"""

import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TestCounts:
    """Current test statistics."""
    total_evals: int
    passed_evals: int
    pytest_discovered: int
    
    @property
    def success_rate(self) -> str:
        """Calculate success percentage."""
        if self.passed_evals == 0:
            return "0%"
        return f"{(self.passed_evals / self.total_evals) * 100:.0f}%"


def get_current_counts() -> TestCounts:
    """Get actual current test counts from filesystem."""
    root = Path(__file__).parent.parent.parent
    
    # Count total eval files
    total_evals = len(list((root / "evals").glob("**/*.md")))
    # Subtract non-test files
    if (root / "evals" / "README.md").exists():
        total_evals -= 1
    if (root / "evals" / "progress.md").exists():
        total_evals -= 1
    
    # Count passed evals
    passed_dir = root / "evals" / "passed"
    passed_evals = len(list(passed_dir.glob("*.md"))) if passed_dir.exists() else 0
    
    # Count pytest-discoverable tests (estimate from passed)
    # Some passed tests might not have valid Cypher, so this is approximate
    pytest_discovered = passed_evals  # Will be refined by actual pytest run if available
    
    return TestCounts(total_evals, passed_evals, pytest_discovered)


def update_file_counts(file_path: Path, counts: TestCounts):
    """Update test counts in a specific file."""
    if not file_path.exists():
        print(f"Warning: {file_path} not found, skipping")
        return
    
    content = file_path.read_text()
    original_content = content
    
    # Patterns to update (flexible to catch variations)
    replacements = [
        # "77 evaluation tests" -> "X evaluation tests"
        (r'\b\d+\s+evaluation\s+tests?\b', f'{counts.total_evals} evaluation tests'),
        
        # "53 EVAL queries" -> "X EVAL queries"  
        (r'\b\d+\s+EVAL\s+queries?\b', f'{counts.passed_evals} EVAL queries'),
        
        # "All 53 surveillance queries" -> "All X surveillance queries"
        (r'\bAll\s+\d+\s+surveillance\s+queries?\b', f'All {counts.passed_evals} surveillance queries'),
        
        # "53 EVAL queries with 100% success" -> "X EVAL queries with Y% success"
        (r'\b\d+\s+EVAL\s+queries?\s+with\s+\d+%\s+success\s+rate?\b', 
         f'{counts.passed_evals} EVAL queries with {counts.success_rate} success rate'),
        
        # "managing 77 evaluation tests" -> "managing X evaluation tests"
        (r'managing\s+\d+\s+evaluation\s+tests?\b', f'managing {counts.total_evals} evaluation tests'),
        
        # "77-question validation suite" -> "X-question validation suite"  
        (r'\b\d+-question\s+validation\s+suite\b', f'{counts.total_evals}-question validation suite'),
        
        # "All 53 tests" -> "All X tests"
        (r'\bAll\s+\d+\s+tests?\b', f'All {counts.passed_evals} tests'),
        
        # "100% Test Success Rate" (keep as-is for passed tests, but could be dynamic)
        # We'll leave this for now since it refers to pytest success rate
    ]
    
    changes_made = []
    for pattern, replacement in replacements:
        new_content, num_subs = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
        if num_subs > 0:
            changes_made.append(f"  {pattern} -> {replacement} ({num_subs} times)")
            content = new_content
    
    if content != original_content:
        file_path.write_text(content)
        print(f"✅ Updated {file_path.relative_to(Path.cwd())}")
        for change in changes_made:
            print(change)
    else:
        print(f"⚪ No changes needed in {file_path.relative_to(Path.cwd())}")


def main():
    """Update all documentation with current test counts."""
    print("🔍 Getting current test counts...")
    counts = get_current_counts()
    
    print(f"""
📊 Current Test Statistics:
   Total Evaluation Tests: {counts.total_evals}
   Passed/Implemented: {counts.passed_evals} 
   Success Rate: {counts.success_rate}
   Pytest Discoverable: {counts.pytest_discovered}
""")
    
    # Files to update
    root = Path(__file__).parent.parent.parent
    files_to_update = [
        root / "README.md",
        root / "docs" / "README.md", 
        root / "docs" / "evaluation-harness-usage.md",
        root / "docs" / "pytest-reports-guide.md",
        root / "tests" / "README.md",
        root / "CLAUDE.md",
        root / "docs" / "index.html",
    ]
    
    print("📝 Updating documentation files...")
    for file_path in files_to_update:
        update_file_counts(file_path, counts)
    
    print(f"""
✅ Update complete! 

To keep counts fresh:
  python scripts/python/update_counts.py

Add to your workflow:
  - After implementing new tests
  - Before creating PRs
  - In CI/CD pipeline
""")


if __name__ == "__main__":
    main()