# MCP Time Server Setup for Claude Code

## Installation

To add the time MCP server to Claude Code, run:

```bash
claude mcp add time "uvx mcp-server-time"
```

This will add the time server to your Claude Code configuration.

## Configuration Options

You can optionally specify a local timezone:

```bash
claude mcp add time "uvx mcp-server-time local-timezone=America/Toronto"
```

## Verification

After adding, verify it's installed:

```bash
claude mcp list
```

You should see:
```
time: uvx mcp-server-time
```

## Usage in Claude Code

The time server provides the following function:

```python
mcp__time__get_current_time(timezone="America/Toronto")
```

Returns:
```json
{
  "timezone": "America/Toronto",
  "datetime": "2025-01-20T22:57:11-05:00",
  "is_dst": false
}
```

## Available Timezones

Common timezone values:
- `America/New_York`
- `America/Toronto`
- `America/Los_Angeles`
- `Europe/London`
- `Europe/Paris`
- `Asia/Tokyo`
- `UTC`

## Example Usage

```python
# Get current time in Toronto
result = mcp__time__get_current_time(timezone="America/Toronto")
date = result["datetime"].split("T")[0]  # Extract date: 2025-01-20
time = result["datetime"].split("T")[1]  # Extract time: 22:57:11-05:00

# Convert between timezones
result = mcp__time__convert_time(
    source_timezone="America/Toronto",
    target_timezone="UTC",
    time="14:30"
)
```

## Troubleshooting

If the time server isn't working:

1. Ensure you have `uvx` installed:
   ```bash
   pip install uvx
   ```

2. Restart Claude Code after adding the server

3. Check the MCP server is running:
   ```bash
   claude mcp list
   ```

## Reference

- **Package**: mcp-server-time
- **Method**: uvx (Python package runner)
- **Documentation**: https://github.com/modelcontextprotocol/servers/tree/main/src/time