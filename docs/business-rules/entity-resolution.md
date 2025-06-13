# Entity Resolution Fallback Logic

**Source**: DGraph analysis  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: High  
**Implementation**: [pending]  

## Problem
When `personname` is missing in session involvements, we need a fallback hierarchy to identify who participated in the session.

## Rule
Use this priority order for entity resolution:

1. `personname` (preferred - human readable name)
2. `msisdn` (phone number) 
3. `email` (email address)
4. `userid` (user identifier)
5. `imei` (device identifier)
6. `imsi` (SIM card identifier)

## Implementation Details
```python
def get_identifier(session, role='From'):
    involvement = [i for i in session.get('involvements') if i.get('role') == role]
    
    if len(involvement) == 0 and role == 'From':
        involvement = [i for i in session.get('involvements') if i.get('role') == 'Participant']
    
    involvement = involvement[0]
    
    involvement_id = involvement.get('personname', 
                     involvement.get('msisdn', 
                     involvement.get('email', 
                     involvement.get('userid', 
                     involvement.get('imei', 
                     involvement.get('imsi', None))))))
    
    return involvement_id
```

## Related
- #fred-travel investigation
- Import script improvements

## Notes
DGraph uses this exact logic successfully. Consider adding validation to ensure we always get some identifier.