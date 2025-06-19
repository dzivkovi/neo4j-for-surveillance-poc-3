## Problem Statement
<!-- What specific capability is missing? Reference evaluation test # if applicable -->

## Evaluation-First Approach
<!-- MANDATORY: Define tests/evals BEFORE implementation -->

### Failing Test
```python
# Example test that MUST fail initially
def test_fred_travel_analysis():
    result = query_fred_travel_mentions()
    assert "Feb 11 2020" in result  # Currently returns empty
    assert "Miami" in result
```

### Success Criteria  
- [ ] Above test passes consistently (5/5 runs)
- [ ] Performance < 5s
- [ ] No modification to original test allowed

## Implementation Notes
<!-- Constraints, validation method (e.g., Neo4j MCP), etc. -->

---
*Remember: Write the eval first. Implementation comes second. Tests are immutable.*
