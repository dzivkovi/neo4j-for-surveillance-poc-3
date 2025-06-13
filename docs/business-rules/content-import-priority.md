# Content Import Priority

**Source**: Client meeting  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: Critical  
**Implementation**: [pending]  

## Problem
Sessions contain multiple document types in the `documents` array. We need to determine which to import and in what priority order.

## Rule
Import document types in this priority order:

1. **Synopsis** (human summaries) - clean but less detail
2. **Automatic Transcription** (full conversations) - complete but messy  
3. **User Comments** (analyst notes) - context clues like "rock salt = code word"

## Implementation Details
```python
def extract_session_content(session):
    content_parts = []
    
    for doc in session.get('documents', []):
        doc_type = doc.get('documenttype', '')
        text = doc.get('text', '')
        
        if doc_type == 'Synopsis' and text:
            content_parts.append(f"SYNOPSIS: {text}")
        elif doc_type == 'Automatic Transcription' and text:
            content_parts.append(f"TRANSCRIPT: {clean_transcript(text)}")
        elif doc_type == 'User Comments' and text:
            content_parts.append(f"ANALYST NOTE: {text}")
    
    return '\n'.join(content_parts)
```

## Related
- #eval-1, #eval-3, #eval-4 (Fred's travel discussions)
- Document content missing from current import

## Notes
Client will provide "alliance" data to help correlate transcripts with business questions.