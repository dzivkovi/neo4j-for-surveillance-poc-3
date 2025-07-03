You are implementing a GitHub issue for the Neo4j surveillance analytics project using evaluation-first development.

**Model Preference**: Use the latest Claude 4 Sonnet model

**Issue to implement:**
$ARGUMENTS

## Workflow

### 1. Analyze Issue
```bash
# If ARGUMENTS is issue number: gh issue view $ARGUMENTS
# If ARGUMENTS is description: search for related issue first
gh issue view $ARGUMENTS
```
- Understand the problem and requirements
- Check if this relates to any of the 77 evaluation tests in `evals/evaluation_tests.md`
- Identify Neo4j MCP validation needs

### 2. Create Work Branch
```bash
# Determine work type based on issue (feat|fix|docs|chore)
# Use issue number and brief description for branch name
git checkout -b <TYPE>/$ARGUMENTS-brief-description

# Examples:
# git checkout -b feat/19-python-formatting-cleanup
# git checkout -b fix/23-neo4j-connection-error
# git checkout -b docs/15-api-documentation-update
# git checkout -b chore/8-dependency-updates
```
- Follow project convention: `<TYPE>/$ISSUE_NUMBER-description`
- Keep description brief but descriptive
- Branch created before any implementation work begins

### 3. Research Codebase
- Read CLAUDE.md for project context and commands
- **Check for design document**: Read `analysis/$ARGUMENTS/DESIGN.md` if it exists
- **Check docs/entity-resolution.md** for entity-resolution context if applicable
- Search for relevant files using available tools
- Understand existing patterns and conventions
- Check current Neo4j schema and data structure using MCP tools

### 4. Write Failing Tests First (Evaluation-First)
**Critical:** Tests define success. Implementation serves tests.
- Write tests that demonstrate the required capability
- Ensure tests fail initially (proves they're testing the right thing)
- Include edge cases and performance requirements
- For AI features: Plan to run tests 5+ times to catch nondeterminism

### 5. Implement Minimal Solution
- Follow existing code patterns and conventions
- Use project libraries and tools (ruff for linting, pytest for testing)
- Implement only what's needed to pass the tests
- Use Neo4j MCP server for live validation during development

### 6. Validation
```bash
# Run tests multiple times (catch AI nondeterminism)
pytest -v  # Run 5+ times for critical tests

# Code quality (120 char line length configured)
ruff format .
ruff check . --fix

# Neo4j validation (use available MCP tools like):
# mcp__neo4j__read_neo4j_cypher(query) - test queries
# mcp__neo4j__get_neo4j_schema() - verify schema
# Verify evaluation test scenarios work
```

### 7. Quality Gates Validation
**Critical:** Cannot proceed until ALL quality gates pass.
```bash
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.claude')))
from workflow.definition_of_done import enforce_definition_of_done
print(enforce_definition_of_done())
"
```

### 8. DESIGN.md Handoff
```bash
mkdir -p analysis/$ARGUMENTS && mv analysis/0000/DESIGN.md analysis/$ARGUMENTS/DESIGN.md
```

### 9. Create Pull Request
```bash
# Use appropriate work type prefix: feat|fix|docs|chore
# Descriptive commit following project patterns
git add -A
git commit -m "<TYPE>: implement [brief description]

- Key changes made
- Evaluation tests now passing
- Neo4j MCP validation confirmed
- All quality gates passing

Closes #$ISSUE_NUMBER"

git push -u origin <TYPE>/$ISSUE_NUMBER-description

# Create PR using template
gh pr create --title "<TYPE>: [Issue title]" --body-file .github/PULL_REQUEST_TEMPLATE.md
```

## Key Principles for This Project

- **Evaluation-First:** Write tests before implementation, run 5+ times
- **Neo4j MCP Validation:** Use MCP tools to validate queries work correctly  
- **Law Enforcement Context:** Remember this serves surveillance analytics use cases
- **Tests are Immutable:** Never modify tests to make implementation easier
- **Less is More:** Simplest solution that passes tests wins
- **Quality Gates:** All automated validation must pass before completion
- **Defensive Programming:** MANDATORY validation after every code change (see CLAUDE.md)

## Project-Specific Notes

- Database: Neo4j with credentials `neo4j`/`Sup3rSecur3!`
- Line length: 120 characters (configured in pyproject.toml)
- Testing: Focus on evaluation tests that verify business requirements
- Performance: Query responses should be <5s for evaluation criteria

Remember: This project must pass real law enforcement evaluation scenarios. Every feature should move us closer to answering those 77 evaluation questions correctly.