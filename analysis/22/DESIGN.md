# Two-Part Solution: Interactive Query Development + Automated Confidence Generation

## Problem / Metric

**Current State**: 29 evaluation tests moved to FAILED during auto-promotion stress testing due to missing confidence data
**Root Cause**: 43 tests have placeholder queries (`// TODO: Implement Cypher query`), others lack confidence calculations
**Key Insights**: 
1. Python scripts cannot "prompt Claude" - need separate interactive and automated workflows
2. Expected values were auto-generated and unreliable - `/eval` should generate everything interactively
3. Business requirements in evaluation_tests.md are vague prose, not numerical targets

## Goal

Implement **Two-Part Solution**:

### Part 1: `/eval NN` Custom Command (Interactive)
- User invokes `/eval 05` to develop query for EVAL-05
- Claude uses Neo4j MCP to test and refine queries interactively
- Updates test file with working Cypher query

### Part 2: Confidence Processor Script (Automated)
- Processes tests with existing confidence sections
- Auto-promotes tests with ≥80% confidence to PASSED
- Simple file parsing - no query execution or calculation
- Reports summary of auto-promotions

## Scope (M/S/W)

### Part 1: `/eval` Command

#### [M] Must Have
- **Command Definition**: Create `.claude/commands/eval.md` with clear workflow
- **Test File Loading**: Search `evals/*/EVAL-NN.md` (abort if multiple found)
- **Interactive Development**: Guide user through query development using MCP
- **File Update**: Replace placeholder with tested Cypher query + confidence assessment

#### [S] Should Have  
- **Context Loading**: Parse row NN from evaluation_tests.md table for business question
- **Query Validation**: Test query before saving to file
- **Error Handling**: Graceful handling of invalid test IDs

### Part 2: Confidence Generator

#### [M] Must Have
- **File Discovery**: Find all test files with `glob.glob('evals/*/EVAL-*.md')`
- **Confidence Parsing**: Extract confidence percentage from existing sections
- **Auto-Promotion**: Move tests with ≥80% confidence to `evals/passed/`
- **Progress Reporting**: Show count of auto-promoted tests

#### [S] Should Have
- **Batch Mode**: Process all eligible tests with progress tracking
- **Skip Reporting**: List tests skipped due to placeholders
- **Error Handling**: Continue processing on query failures

#### [W] Won't Have
- **Automated Query Generation**: No AI or intelligent parsing
- **Cross-Script Communication**: No integration between Part 1 and Part 2
- **State Management**: No automatic file moves (leave to existing harness)

## Acceptance Criteria

### Part 1: `/eval` Command

| # | Given | When | Then |
|---|-------|------|------|
| 1 | EVAL-05 has placeholder query | User runs `/eval 05` | Claude opens EVAL-05.md, shows business question, guides query development |
| 2 | User approves developed query | Claude tests query via MCP | Query is validated and file is updated with working Cypher |
| 3 | Invalid test ID provided | User runs `/eval 999` | Error message shows valid range (01-77) |
| 4 | Test already has non-placeholder query | User runs `/eval 03` | Claude shows existing query and asks if user wants to improve it |

### Part 2: Confidence Generator

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Test with existing confidence section | Script parses file | Confidence percentage extracted |
| 2 | Test with ≥80% confidence | Script processes file | Test auto-promoted to `evals/passed/` |
| 3 | Test with 31-79% confidence | Script processes file | Test remains in current directory |
| 4 | Test with ≤30% confidence | Script processes file | Test auto-failed to `evals/failed/` |
| 5 | Test without confidence section | Script encounters file | Test skipped (needs `/eval` command first) |
| 6 | Batch mode invoked | User runs script | Summary report shows auto-promotion count |
| 7 | File parsing fails | Malformed confidence section | Test skipped, error logged, continues |

## Technical Implementation

### Part 1: `/eval` Command

**Command File**: `.claude/commands/eval.md`
```markdown
---
description: Develop Cypher query for evaluation test
arguments: test_number
---
Opens EVAL-NN test file and guides interactive query development using Neo4j MCP
```

**Workflow**:

1. Parse test number, search `evals/*/EVAL-NN.md` (abort if multiple)
2. Parse row NN from evaluation_tests.md table for business question (consult source - business folks often say vague things like "see above")
3. Use MCP to explore schema and test queries interactively (same "dance" approach used successfully before)
4. Show query results and ask: "Does this correctly answer the business question? (Y/N/Partial)"
5. Generate confidence: Y=80%, Partial=70%, N=30%
6. Update file with working query + confidence section

**Implementation Note**: Use "abort on error & ask human operator to fix" approach - just like interactive Claude Code mode. This is a personal project with manageable scope.

### Part 2: Simplified Confidence Processor

**Add to**: `evaluation_harness.py`
```python
import re
import glob
import os

def process_existing_confidence(self, test_id=None, batch=False):
    """Process tests with existing confidence sections for auto-promotion"""
    
    # Find test files - handle ID to path conversion properly
    if test_id:
        # Convert test ID to file path pattern (handles both "05" and "EVAL-05")
        clean_id = test_id.replace("EVAL-", "").zfill(2)
        test_files = glob.glob(f'evals/*/EVAL-{clean_id}.md')
    else:
        test_files = glob.glob('evals/*/EVAL-*.md')
        
    promoted_count = 0
    failed_count = 0
    
    for test_file in test_files:
        # Parse existing confidence section
        confidence_data = self._parse_confidence_section(test_file)
        
        if confidence_data:
            # Extract test ID from file path for transition_test
            filename = os.path.basename(test_file)
            test_id = filename.replace('.md', '')
            
            if confidence_data['percentage'] >= 80:
                # Use existing harness transition method
                self.transition_test(test_id, TestState.REVIEW, TestState.PASSED)
                promoted_count += 1
                print(f"Auto-promoted {test_id} with {confidence_data['percentage']}% confidence")
            elif confidence_data['percentage'] <= 30:
                # Use existing harness transition method  
                self.transition_test(test_id, TestState.REVIEW, TestState.FAILED)
                failed_count += 1
                print(f"Auto-failed {test_id} with {confidence_data['percentage']}% confidence")
            # 31-79% stays in current location (REVIEW)
    
    print(f"Auto-promoted {promoted_count} tests, auto-failed {failed_count} tests")

def _parse_confidence_section(self, test_file):
    """Extract confidence percentage from existing confidence sections"""
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Look for new simple format (all three cases)
    patterns = [
        r'Confidence: (\d+)% → Auto-promote to PASSED',
        r'Confidence: (\d+)% → Auto-fail to FAILED', 
        r'Confidence: (\d+)% → Stay in REVIEW'
    ]
    
    for pattern in patterns:
        confidence_match = re.search(pattern, content)
        if confidence_match:
            return {'percentage': int(confidence_match.group(1))}
    
    return None
```

**Key Simplification**: Part 2 only reads existing confidence sections created by `/eval` command (Part 1), eliminating complex query execution and confidence calculation logic.

### Legacy Confidence Handling

**Simple Rule**: Ignore old complex confidence calculations. Only recognize new format:

- ✅ **New Format**: `Confidence: 80% → Auto-promote to PASSED`
- ❌ **Ignore**: `Confidence = (count_accuracy × 0.7) + (score_similarity × 0.3)`

This ensures clean transition without breaking existing working tests or confusing implementation.

### Business-Friendly Confidence Assessment

The `/eval` command uses simple human judgment instead of complex algorithms:

```markdown
## Confidence Assessment

**Query Results**: [actual results shown to user]
**Business Question**: "what is in the shed?"
**Assessment**: Does this correctly answer the business question?

- ✅ **Y** = 80% confidence (auto-promotes to PASSED)
- ⚠️ **Partial** = 30% < confidence < 80% (stays in REVIEW)
- ❌ **N** = 30% confidence (auto-fails to FAILED)

**Confidence**: 80% → Auto-promote to PASSED
```

**Complete Triaging System**:

- **≥80%** = Auto-promote to PASSED ✅
- **31-79%** = Stay in REVIEW for human decision ⚠️
- **≤30%** = Auto-fail to FAILED ❌

**Benefits**:

- ✅ No complex math for business users
- ✅ Human judgment where it matters
- ✅ Simple Y/N/Partial decision
- ✅ Automatic handling of clear wins and clear failures
- ✅ Reduces manual review workload on both ends

### Expected Outcome

**43 tests with placeholders** → Use `/eval NN` command interactively (generates query + confidence)
**Tests with existing confidence** → Part 2 processes for auto-promotion (reads existing confidence sections)
**Result**: Clear separation between interactive development and automated processing

### Validation Status

✅ **Simplified design validated**: Expected values discovered to be auto-generated and unreliable
✅ **Interactive workflow confirmed**: `/eval` command can generate both query and confidence during development
✅ **File parsing approach proven**: Existing confidence sections use consistent format for easy parsing
✅ **Separation of concerns achieved**: Interactive development (Part 1) vs automated processing (Part 2)
✅ **Implementation complexity minimized**: Following perfection principle "nothing left to take away"

## Design Evolution

This design went through multiple iterations to reach the current simplified form:

### Initial Version (Over-engineered)

- **Part 1**: Complex AI-powered query generator with intelligent parsing
- **Part 2**: Expected/actual comparison using database queries + complex confidence calculation
- **Problems**: Massive scope, would take months to implement, violated perfection principle

### Second Version (MCP Integration Blocker)

- **Part 1**: Interactive `/eval` command (✅ good)
- **Part 2**: MCP tool integration for query execution
- **Problems**: MCP tools not accessible from Python scripts - architectural blocker

### Third Version (Direct Neo4j Connection)

- **Part 1**: Interactive `/eval` command (✅ good)
- **Part 2**: Direct Neo4j connection with expected/actual comparison
- **Problems**: Missing expected value sources, complex parsing logic

### Final Version (Simplified)

- **Part 1**: Interactive `/eval` command generates **both query and confidence**
- **Part 2**: Simple file parser reads existing confidence sections
- **Result**: Minimal implementation following "nothing left to take away" principle

### Key Breakthrough

**User insight**: "I see those expected values were auto generated"

This revelation eliminated the entire expected/actual comparison problem. Since business requirements are vague prose ("Semantic search to find 'Kenzie'... Combination search..."), the `/eval` command should generate confidence during the interactive session when a human can assess quality.

---
*Implementation-ready design using validated technical approach. No architectural blockers remain.*
