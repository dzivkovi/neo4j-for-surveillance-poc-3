# Search Similarity Thresholds

**Source**: DGraph comparison analysis  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: Medium  
**Implementation**: [pending]  

## Problem
Need to determine appropriate similarity thresholds for semantic search to balance precision vs recall.

## Rule
- **Exact text matches**: score = 1.0 (highest priority)
- **Semantic similarity**: threshold = 0.7 (DGraph standard)
- **Lower threshold**: more results but potentially less relevant
- **Higher threshold**: fewer but more precise results

## Implementation Details
```python
def hybrid_search(query, threshold=0.7):
    # 1. Exact text matches (score = 1.0)
    exact_matches = full_text_search(query)
    
    # 2. Semantic similarity
    semantic_matches = vector_search(query, threshold)
    
    # 3. Combine and rank
    return combine_results(exact_matches, semantic_matches)
```

## Related
- Fred investigation search failures
- DGraph hybrid search implementation

## Notes
Need to tune threshold based on our specific use case and content quality. Consider making it configurable per query type.