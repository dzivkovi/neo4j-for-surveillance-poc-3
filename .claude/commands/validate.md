# Validation Command

Runs comprehensive validation checks after code changes.

## Usage
```bash
/validate
```

## What this command does

This command runs defensive programming validation checks to ensure code changes are complete and working:

1. **Search validation**: Finds any remaining instances of old patterns
2. **Test validation**: Runs relevant test suites
3. **Functional validation**: Tests actual functionality
4. **Integration validation**: Checks database connections and queries

## Arguments
$ARGUMENTS can contain:
- `--pattern <pattern>`: Specific pattern to search for (e.g., "content_vector_index")
- `--tests <path>`: Specific test file/directory to run (e.g., "tests/test_openai_embeddings.py")
- `--skip-search`: Skip comprehensive search validation
- `--skip-tests`: Skip test suite execution

## Examples
```bash
/validate --pattern "content_vector_index" --tests "tests/test_openai_embeddings.py"
/validate --skip-search
/validate
```

## Validation Steps

### 1. Search Validation
- Uses `rg` to find any remaining instances of patterns that should be changed
- Reports exact files and line numbers
- **FAILS** if unexpected occurrences found

### 2. Test Validation  
- Runs pytest on affected test files
- **FAILS** if any tests fail
- Reports test coverage and results

### 3. Database Validation
- Tests Neo4j connections
- Validates Cypher queries if modified
- Checks index status and functionality

### 4. Functional Validation
- Runs sample queries/operations
- Verifies end-to-end functionality
- **FAILS** if core features broken

## Success Criteria
✅ All validations must pass before declaring changes complete
✅ Zero unexpected pattern occurrences  
✅ All tests passing
✅ Database operations working
✅ Sample functionality confirmed

## Failure Response
❌ If any validation fails:
1. Report exact failure details
2. Create TodoWrite with specific fixes needed
3. **DO NOT** proceed with commits
4. Fix issues and re-run validation