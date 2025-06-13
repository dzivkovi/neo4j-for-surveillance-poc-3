# Location Tracking Extraction

**Source**: DGraph comparison analysis  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: Low  
**Implementation**: [pending]  

## Problem
Session data contains GPS coordinates in `trackpoints` array that could be used for location-based investigations.

## Rule
Extract and use location data from sessions:

1. **trackpoints**: Contains GPS coordinates with timestamps
2. **Location nodes**: Create geographic entities
3. **Tracking relationships**: Link sessions to locations

## Implementation Details
```python
# Extract from session:
trackpoints = session.get('trackpoints', [])
for point in trackpoints:
    latitude = point.get('latitude')
    longitude = point.get('longitude') 
    timestamp = point.get('timestamp')
    
# Create Location nodes:
location = Location(
    coordinates=[longitude, latitude],
    timestamp=timestamp
)

# Relationships:
Session -[:OCCURRED_AT]-> Location
Person -[:TRACKED_AT]-> Location (if istarget=true)
```

## Related
- Enhanced investigation capabilities
- Geographic analysis queries
- DGraph location functionality

## Notes
DGraph demonstrates location queries like "average person location" and city boundary detection. Consider if this level of geo-analysis is needed.