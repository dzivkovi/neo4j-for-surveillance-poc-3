# KeyFields Metadata Usage

**Source**: Fred travel investigation analysis  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: Low  
**Implementation**: [pending]  

## Problem
Sessions contain `keyfields` metadata with investigation flags that aren't being used for search or categorization.

## Rule
Import and index keyfields for investigative filtering:

**Common keyfields found:**
- "Money Transfer" 
- "PC for Search Warrant"
- "Self Identify"

## Implementation Details
```python
# Extract from session:
keyfields = session.get('keyfields', [])
for field in keyfields:
    name = field.get('name')
    value = field.get('value')
    
# Options:
# 1. Session properties
session.money_transfer = get_keyfield_value(keyfields, 'Money Transfer')

# 2. Separate KeyField nodes  
keyfield = KeyField(name=name, value=value)
session -[:HAS_FLAG]-> keyfield

# 3. Tags/labels
if money_transfer_flag:
    session:MoneyTransfer
```

## Related
- Enhanced search capabilities
- Investigation categorization
- Metadata completeness

## Notes
Need to understand full list of possible keyfields and their business meaning before implementing indexing strategy.