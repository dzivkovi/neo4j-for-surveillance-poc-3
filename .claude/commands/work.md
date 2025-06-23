You are implementing a GitHub issue for the Neo4j surveillance analytics project using evaluation-first development.

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

### 2. Research Codebase
- Read CLAUDE.md for project context and commands
- **Check for design document**: Read `analysis/$ARGUMENTS/DESIGN.md` if it exists
- Search for relevant files using available tools
- Understand existing patterns and conventions
- Check current Neo4j schema and data structure

### 3. Write Failing Tests First (Evaluation-First)
**Critical:** Tests define success. Implementation serves tests.
- Write tests that demonstrate the required capability
- Ensure tests fail initially (proves they're testing the right thing)
- Include edge cases and performance requirements
- For AI features: Plan to run tests 5+ times to catch nondeterminism

### 4. Implement Minimal Solution
- Follow existing code patterns and conventions
- Use project libraries and tools (ruff for linting, pytest for testing)
- Implement only what's needed to pass the tests
- Use Neo4j MCP server for live validation during development

### 5. Validation
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

### 6. Create Pull Request
```bash
# Descriptive commit following project patterns
git add -A
git commit -m "feat: implement [brief description]

- Key changes made
- Evaluation tests now passing
- Neo4j MCP validation confirmed

Closes #$ISSUE_NUMBER

git push -u origin feat/$ISSUE_NUMBER-description

# Create PR using template
gh pr create --title "feat: [Issue title]" --body-file .github/PULL_REQUEST_TEMPLATE.md
```

## Key Principles for This Project

- **Evaluation-First:** Write tests before implementation, run 5+ times
- **Neo4j MCP Validation:** Use MCP tools to validate queries work correctly  
- **Law Enforcement Context:** Remember this serves surveillance analytics use cases
- **Tests are Immutable:** Never modify tests to make implementation easier
- **Less is More:** Simplest solution that passes tests wins

## Project-Specific Notes

- Database: Neo4j with credentials `neo4j`/`Sup3rSecur3!`
- Line length: 120 characters (configured in pyproject.toml)
- Testing: Focus on evaluation tests that verify business requirements
- Performance: Query responses should be <5s for evaluation criteria

Remember: This project must pass real law enforcement evaluation scenarios. Every feature should move us closer to answering those 77 evaluation questions correctly.