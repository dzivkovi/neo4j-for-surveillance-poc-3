#!/usr/bin/env python3
"""
Update test counts across all documentation files.

Single source of truth for test statistics.
Run this after any changes to keep documentation in sync.
"""

import re
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


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
    
    # Count total eval files (only EVAL-NN.md pattern)
    total_evals = len(list((root / "evals").glob("**/EVAL-*.md")))
    
    # Count passed evals
    passed_dir = root / "evals" / "passed"
    passed_evals = len(list(passed_dir.glob("*.md"))) if passed_dir.exists() else 0
    
    # Count pytest-discoverable tests (estimate from passed)
    # Some passed tests might not have valid Cypher, so this is approximate
    pytest_discovered = passed_evals  # Will be refined by actual pytest run if available
    
    return TestCounts(total_evals, passed_evals, pytest_discovered)


def get_evaluation_prompts() -> Dict[str, str]:
    """Get actual prompts from evaluation_tests.md source file."""
    root = Path(__file__).parent.parent.parent
    eval_file = root / "evals" / "evaluation_tests.md"
    
    if not eval_file.exists():
        print(f"Warning: {eval_file} not found")
        return {}
    
    content = eval_file.read_text()
    
    # Extract table rows: | # | Theme | Prompt | Expected Response | Categories |
    table_pattern = r'\|\s*(\d+)\s*\|\s*[^|]+\s*\|\s*([^|]+)\s*\|\s*[^|]+\s*\|\s*[^|]+\s*\|'
    
    prompts = {}
    for match in re.finditer(table_pattern, content):
        number = int(match.group(1))
        prompt = match.group(2).strip()
        eval_id = f"EVAL-{number:02d}"
        
        # Truncate long prompts for table readability
        if len(prompt) > 80:
            prompt = prompt[:77] + "..."
        
        prompts[eval_id] = prompt
    
    return prompts


def update_eval_files_with_benchmarks():
    """Run benchmarks and update individual EVAL-xx.md files with results."""
    root = Path(__file__).parent.parent.parent
    
    try:
        # Run pytest benchmark and capture JSON output to temp file
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        result = subprocess.run([
            "pytest", "tests/test_eval_queries.py::test_eval_performance",
            "--benchmark-only", f"--benchmark-json={tmp_path}", "-q"
        ], cwd=root, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"Warning: Benchmark failed: {result.stderr}")
            os.unlink(tmp_path)
            return
        
        # Read JSON from temp file
        with open(tmp_path, 'r') as f:
            data = json.load(f)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Get benchmark timestamp
        benchmark_timestamp = data.get('datetime', datetime.now().isoformat())
        formatted_timestamp = format_timestamp(benchmark_timestamp)
        
        # Update individual EVAL files with benchmark results
        for bench in data.get('benchmarks', []):
            name = bench['name']
            match = re.search(r'EVAL-\d+', name)
            if match:
                eval_id = match.group(0)
                seconds = bench['stats']['mean']
                
                # Format duration appropriately
                if seconds < 0.001:  # Less than 1ms
                    duration_ms = f"{seconds * 1000:.0f}μs"
                elif seconds < 1:  # Less than 1 second  
                    duration_ms = f"{seconds * 1000:.1f}ms"
                else:
                    duration_ms = f"{seconds * 1000:.0f}ms"
                
                # Find and update the EVAL file
                for status_dir in ['passed', 'failed', 'review', 'blocked']:
                    eval_file = root / 'evals' / status_dir / f'{eval_id}.md'
                    if eval_file.exists():
                        content = eval_file.read_text()
                        
                        # Update Last-Run timestamp
                        content = re.sub(
                            r'Last-Run:\s*[^\n]*',
                            f'Last-Run: {benchmark_timestamp}',
                            content
                        )
                        
                        # Update Duration-ms
                        content = re.sub(
                            r'Duration-ms:\s*[^\n]*',
                            f'Duration-ms: {duration_ms}',
                            content
                        )
                        
                        eval_file.write_text(content)
                        print(f"✅ Updated {eval_file.relative_to(root)} with benchmark data")
                        break
        
    except Exception as e:
        print(f"Warning: Could not update EVAL files with benchmark data: {e}")


def format_timestamp(timestamp_str: str) -> str:
    """Convert ISO timestamp to human-readable EST format."""
    if not timestamp_str or timestamp_str == "—":
        return "—"
    
    try:
        # Handle different timestamp formats
        if 'T' in timestamp_str:
            # ISO format like "2025-07-03T09:27:52.037657"
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        else:
            # Simple date format like "2025-07-03"
            if len(timestamp_str) == 10:  # YYYY-MM-DD
                return timestamp_str  # Already in good format
            dt = datetime.fromisoformat(timestamp_str)
        
        # Format as human readable (EST assumed)
        return dt.strftime("%Y-%m-%d %H:%M")
        
    except Exception:
        # If parsing fails, return as-is
        return timestamp_str


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


def update_dashboard(counts: TestCounts, prompts: Dict[str, str]):
    """Update the evaluation dashboard reading from EVAL files (single source of truth)."""
    root = Path(__file__).parent.parent.parent
    
    # Get current evaluation statuses from file structure
    statuses = {}
    status_dirs = {
        "passed": "✅",
        "failed": "❌", 
        "review": "🟠",
        "blocked": "⏸"
    }
    
    for dir_name, status_symbol in status_dirs.items():
        status_dir = root / "evals" / dir_name
        if status_dir.exists():
            for eval_file in status_dir.glob("EVAL-*.md"):
                eval_id = eval_file.stem
                
                # Extract all data from the EVAL file itself
                try:
                    content = eval_file.read_text()
                    
                    # Get Last-Run or fallback to Added
                    last_run_match = re.search(r'Last-Run:\s*([^\n]+)', content)
                    last_run = last_run_match.group(1).strip() if last_run_match else "—"
                    
                    if last_run == "—":
                        # Fallback to Added date
                        added_match = re.search(r'Added:\s*([^\n]+)', content)
                        last_run = added_match.group(1).strip() if added_match else "—"
                    
                    # Format timestamp for readability
                    last_run = format_timestamp(last_run)
                    
                    # Get Duration-ms from file
                    duration_match = re.search(r'Duration-ms:\s*([^\n]+)', content)
                    duration = duration_match.group(1).strip() if duration_match else "—"
                    
                    # Determine notes based on status
                    notes = "—"
                    if status_symbol == "❌":
                        if "overfitted" in content.lower():
                            notes = "Overfitted implementation - requires native GenAI features"
                        elif "text2cypher" in content.lower() or "graphrag" in content.lower():
                            notes = "Requires text2cypher/GraphRAG redesign"
                    elif status_symbol == "⏸":
                        notes = "Framework feature - not core Neo4j functionality"
                        
                except Exception:
                    last_run = "—"
                    duration = "—"
                    notes = "—"
                
                statuses[eval_id] = {
                    'status': status_symbol,
                    'last_run': last_run,
                    'duration': duration,
                    'notes': notes
                }
    
    # Count statuses for summary
    status_counts = {"✅": 0, "❌": 0, "🟠": 0, "⏸": 0, "⬜": 0}
    for status_info in statuses.values():
        status_counts[status_info['status']] += 1
    
    # Calculate missing tests (⬜)
    status_counts["⬜"] = counts.total_evals - sum(status_counts[s] for s in ["✅", "❌", "🟠", "⏸"])
    
    # Generate dashboard content
    dashboard = f"""# Evaluation Progress Dashboard

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Tests**: {counts.total_evals}

## Status Summary

- ⬜ **TODO**: {status_counts["⬜"]}
- 🟠 **REVIEW**: {status_counts["🟠"]}
- ✅ **PASSED**: {status_counts["✅"]}
- ❌ **FAILED**: {status_counts["❌"]}
- ⏸ **BLOCKED**: {status_counts["⏸"]}

## Test Details

| ID | Prompt | Status | Last Run | Duration | Notes |
|----|--------|---------|-----------|-----------|---------|
"""
    
    # Generate table rows for all evaluations
    for i in range(1, counts.total_evals + 1):
        eval_id = f"EVAL-{i:02d}"
        
        # Get prompt (fallback to generic if not found)
        prompt = prompts.get(eval_id, "Unknown requirement")
        
        # Get status info from files
        status_info = statuses.get(eval_id, {
            'status': '⬜',
            'last_run': '—',
            'duration': '—',
            'notes': 'Not implemented'
        })
        
        dashboard += f"| {eval_id} | {prompt} | {status_info['status']} | {status_info['last_run']} | {status_info['duration']} | {status_info['notes']} |\n"
    
    dashboard += """
## Legend
- ⬜ Todo
- 🟠 Review
- ✅ Passed
- ❌ Failed
- ⏸ Blocked
"""
    
    # Write dashboard
    dashboard_file = root / "evals" / "README.md"
    dashboard_file.write_text(dashboard)
    print(f"✅ Updated dashboard: {dashboard_file.relative_to(Path.cwd())}")


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
    
    # First: Update EVAL files with fresh benchmark data (source of truth)
    print("🔬 Updating EVAL files with benchmark data...")
    update_eval_files_with_benchmarks()
    
    # Then: Generate dashboard from updated EVAL files
    print("📊 Updating evaluation dashboard...")
    prompts = get_evaluation_prompts()
    update_dashboard(counts, prompts)
    
    # Files to update (excluding evals/README.md since we just updated it)
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
✅ Complete update finished! 

Single command for future updates:
  python scripts/python/update_counts.py

This now includes:
  - Evaluation dashboard with proper prompts and benchmark data
  - All documentation with current test counts
  - Consistent numbers across all files

Use before:
  - Creating PRs or commits
  - Client presentations
  - Major releases
""")


if __name__ == "__main__":
    main()