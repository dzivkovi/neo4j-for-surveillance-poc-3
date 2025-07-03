# Design Document: Python Code Formatting Cleanup

## Overview
This task involves standardizing Python code formatting across the entire codebase using the project's established `ruff` configuration.

## Problem Statement
During development of other features, inconsistent Python formatting was discovered across multiple files. This creates:
- Inconsistent code style that hampers readability
- Potential merge conflicts in the future
- Violation of project coding standards outlined in CONTRIBUTING.md

## Technical Approach

### Files Requiring Formatting
Based on analysis, the following files need formatting:
- `.claude/workflow/*.py` (multiple files)
- `scripts/python/02-import-transcripts.py`  
- `scripts/python/03-graphrag-demo.py`
- `scripts/python/extract-sessions.py`
- `tests/test_work_automation.py`

### Implementation Strategy
1. Run `ruff format .` on entire codebase to ensure consistent formatting
2. Run `ruff check . --fix` to auto-fix linting issues
3. Commit changes as a single chore commit
4. Establish this as part of pre-commit workflow going forward

### Quality Assurance
- Verify no functional changes occur (formatting only)
- Ensure all existing tests continue to pass
- Confirm ruff configuration compliance (pyproject.toml settings)

## Non-Goals
- This does not involve functional code changes
- Does not modify ruff configuration itself
- Does not impact any business logic or features

## Acceptance Criteria
- [ ] All Python files pass `ruff format .` with no changes needed
- [ ] All Python files pass `ruff check .` with no errors
- [ ] All existing tests continue to pass
- [ ] Changes committed with appropriate `chore:` prefix

## Implementation Notes
This is a one-time cleanup task that was separated from feature development to maintain clean commit history and PR scope.