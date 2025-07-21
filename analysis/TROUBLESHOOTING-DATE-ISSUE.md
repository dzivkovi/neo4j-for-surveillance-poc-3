# DATE PARSING TROUBLESHOOTING

## The Problem
I consistently mistake July (07) for January (01) when creating date-based folders.

## Evidence
- MCP server returns: `"datetime": "2025-07-20T23:04:42-04:00"`
- I create folder: `analysis/2025-01-20/` (WRONG - January instead of July)

## Root Cause Analysis
The datetime string format is ISO 8601: `YYYY-MM-DDTHH:MM:SS±HH:MM`
- Year: 2025 ✓
- Month: 07 (July) - I incorrectly use 01 (January)
- Day: 20 ✓

## Solution for Future
When extracting date from MCP time server response:
1. Get the full datetime string
2. Split on 'T' to get date portion: `datetime.split('T')[0]`
3. This gives: `2025-07-20` (NOT `2025-01-20`)

## Corrected Process
```python
# From MCP response
datetime = "2025-07-20T23:04:42-04:00"
date = datetime.split('T')[0]  # "2025-07-20"
# Create folder: analysis/2025-07-20/
```

## Note to Self
ALWAYS double-check the month extraction. July is 07, not 01!