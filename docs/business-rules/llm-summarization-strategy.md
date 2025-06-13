# LLM Summarization Strategy

**Source**: DGraph comparison analysis  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: Medium  
**Implementation**: [pending]  

## Problem
DGraph uses LLM-generated summaries and topic extraction for better search performance and cached results.

## Rule
Implement LLM processing pipeline for:

1. **Call Summaries**: Generate concise summaries optimized for embedding
2. **Topic Extraction**: Extract main topics using structured JSON output  
3. **Caching Strategy**: Store summaries as separate nodes to avoid re-computing

## Implementation Details
```python
# DGraph uses Mistral Small for:
def get_transcript_summary(transcript):
    # Generate summary < 512 tokens, optimized for embeddings
    
def get_transcript_topics(transcript):  
    # Extract topics as JSON array of strings
    # Examples: ['gambling', 'travel', 'business operations']
    
# Cache in graph:
Summary -> Person (summarized_in)
Summary -> Call (summarized_by)
Topic -> Call (discussed)
```

## Related
- Content import improvements
- Performance optimization
- Search enhancement

## Notes
Consider cost implications of LLM processing vs search performance gains. May want to implement selectively for high-priority content first.