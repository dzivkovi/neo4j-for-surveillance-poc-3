# Transcript Parsing Format

**Source**: Fred travel investigation analysis  
**Date**: 2025-06-13  
**Status**: TODO  
**Priority**: High  
**Implementation**: [pending]  

## Problem
Automatic Transcription documents contain timestamped dialog that needs proper parsing to extract clean conversation text.

## Rule
Parse transcript format consistently:

**Format**: `00:00:05 -> 00:00:05 [en]\nDialog text here.`

## Implementation Details
```python
def parse_transcript(transcript_text):
    """Extract dialog from timestamped transcript"""
    dialog_lines = []
    
    lines = transcript_text.split('\n')
    for line in lines:
        if '->' in line and '[en]' in line:
            # Split on language marker
            parts = line.split('[en]')
            if len(parts) > 1:
                dialog = parts[1].strip()
                if dialog:  # Skip empty lines
                    dialog_lines.append(dialog)
    
    return '\n'.join(dialog_lines)

# Example input:
# "00:00:05 -> 00:00:05 [en]\nTalk to me.\n00:00:06 -> 00:00:07 [en]\nYou placed your bet yet?"

# Example output:
# "Talk to me.\nYou placed your bet yet?"
```

## Related
- Content import priority
- Fred travel investigation
- #eval-1, #eval-3, #eval-4

## Notes
May need to handle multi-language transcripts differently. Consider preserving timestamps for temporal queries.