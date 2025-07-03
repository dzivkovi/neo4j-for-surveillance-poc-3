# Evaluation Test Harness v2 - Usage Guide

This guide explains how to use the Evaluation Test Harness v2 system for managing Neo4j evaluation tests.

## Overview

The Evaluation Test Harness provides a git-native workflow for managing 77 evaluation tests through a 5-state system:

- **TODO**: Tests not yet implemented
- **REVIEW**: Tests implemented but need verification
- **PASSED**: Tests that successfully validate expected behavior
- **FAILED**: Tests that don't match expected results
- **BLOCKED**: Tests that can't be implemented (e.g., require external features)

## Quick Start

### 1. Initial Migration (One-time Setup)

If you have existing `evals/implemented/` and `evals/pending/` folders:

```bash
python scripts/python/evaluation_harness.py migrate --evals-dir evals
```

This will:
- Move implemented tests → `review/` folder
- Move pending tests → `todo/` folder
- Create stub files for all missing tests (up to 77 total)
- Add machine-readable headers to all files
- Remove old folder structure

### 2. Running Tests

To run a specific evaluation test:

```bash
python scripts/python/evaluation_harness.py run --test-id EVAL-03
```

The harness will:
- Execute the test (currently simplified - future versions will run actual Cypher)
- Update the test's metadata (run count, duration, last run time)
- Automatically move the file to appropriate state folder based on results

### 3. Generate Progress Dashboard

To see current status of all tests:

```bash
python scripts/python/evaluation_harness.py dashboard --evals-dir evals
```

This creates/updates `evals/progress.md` with:
- Status summary (counts by state)
- Detailed table of all 77 tests
- Visual indicators (⬜ TODO, 🟠 REVIEW, ✅ PASSED, ❌ FAILED, ⏸ BLOCKED)

### 4. Export to CSV

For business users who prefer spreadsheets:

```bash
python scripts/python/evaluation_harness.py csv --evals-dir evals
```

Creates `evals/progress.csv` with test status for Excel/Google Sheets.

## File Structure

### Machine-Readable Headers

Each evaluation file starts with a metadata header:

```markdown
<!--- META: machine-readable for scripts --->
Status: REVIEW
ID: EVAL-03
Category: Search
Added: 2025-07-03
Last-Run: 2025-07-03T10:30:00
Duration-ms: 125
Run-Count: 3
Blocker: —

# EVAL-03: Does <@Merlin, Fred> discuss travel plans?
```

### Folder Organization

```
evals/
├── todo/        # Tests to implement
├── review/      # Tests needing verification
├── passed/      # Validated tests
├── failed/      # Tests with issues
├── blocked/     # Tests that can't be implemented
├── template.md  # Template for new tests
└── progress.md  # Generated dashboard
```

## Workflow Examples

### 1. Implementing a TODO Test

1. Find test in `todo/` folder
2. Add Cypher query and expected results
3. Run the test: `python scripts/python/evaluation_harness.py run --test-id EVAL-XX`
4. Test automatically moves to `review/` or `passed/` based on results

### 2. Debugging a Failed Test

1. Test appears in `failed/` folder after execution
2. Review the query and expected results
3. Fix the implementation
4. Re-run the test to move it to `passed/`

### 3. Business User Review

1. Generate dashboard: `python scripts/python/evaluation_harness.py dashboard`
2. Export to CSV: `python scripts/python/evaluation_harness.py csv`
3. Review in Excel/Google Sheets
4. Add comments or blockers to specific tests

## State Transitions

Tests move between states based on:

- **TODO → REVIEW**: When test is implemented (manual edit)
- **REVIEW → PASSED**: When test execution matches expected results with ≥80% confidence (automatic)
- **REVIEW → FAILED**: When test execution doesn't match expectations
- **ANY → BLOCKED**: When test can't be implemented (manual with blocker reason)

All transitions use `git mv` to maintain version history.

### Auto-Promotion Logic

The harness automatically promotes tests from REVIEW → PASSED when **confidence ≥ 80%**.

**Confidence Calculation**:

```text
Confidence = (count_accuracy × 0.7) + (score_similarity × 0.3)

Where:
- count_accuracy = min(actual_count, expected_count) / expected_count  
- score_similarity = 1 - abs(actual_score - expected_score) / expected_score
```

**Examples**:

- EVAL-06: (14/14 × 0.7) + (2.84/2.82 × 0.3) = **98% confidence** → Auto-promote
- EVAL-03: (12/12 × 0.7) + (5.37/5.37 × 0.3) = **100% confidence** → Auto-promote

**Manual Review Required** when:

- Confidence < 80%
- Missing expected results data
- Query execution errors
- Business logic validation needed

## Integration with Git

Since all state changes are file moves:

```bash
# See which tests changed state
git status

# Commit test implementations
git add evals/review/EVAL-05.md
git commit -m "feat: implement EVAL-05 shed content search"

# Review test history
git log --follow evals/passed/EVAL-03.md
```

## Technical Implementation Notes

### Key Components

1. **TestState Enum** (`evaluation_harness.py:18`): Defines the 5 states
2. **TestFile Dataclass** (`evaluation_harness.py:38`): Parses and updates test metadata
3. **EvaluationHarness** (`evaluation_harness.py:135`): Main orchestrator for test lifecycle
4. **ProgressDashboard** (`evaluation_harness.py:288`): Generates reports

### Adding New Features

The system is designed to be extended. Future enhancements could include:

- Neo4j MCP integration for actual query execution
- Automated test discovery from query patterns
- Performance benchmarking
- Test categorization and filtering
- CI/CD integration for continuous validation

## Tips for Success

1. **Use git branches**: Create feature branches for implementing sets of tests
2. **Commit often**: Each test implementation is a logical commit
3. **Document blockers**: When marking tests as BLOCKED, explain why
4. **Review regularly**: Generate dashboards weekly to track progress
5. **Collaborate**: The markdown format allows easy PR reviews

## Troubleshooting

### "Test file not found"

- Ensure test ID matches exactly (e.g., EVAL-03, not eval-03)
- Check that file exists in one of the state folders

### Migration issues

- Backup `evals/` folder before migration
- Ensure no uncommitted changes in eval files
- Run with `--dry-run` first (if implemented)

### Parse errors

- Verify machine-readable header format is intact
- Check for UTF-8 encoding issues
- Ensure no manual edits broke the header structure

## Future Roadmap

This is v2 of the evaluation harness. Planned improvements:

1. **Neo4j Integration**: Direct query execution via MCP
2. **Parallel Execution**: Run multiple tests concurrently
3. **Performance Tracking**: Historical performance trends
4. **Custom Categories**: Beyond the current classification
5. **Web UI**: Optional web interface for non-technical users

For questions or contributions, see the main project README.