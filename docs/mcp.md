# Neo4j MCP (Model Context Protocol) Integration

## Natural Language Access to Graph Databases

This document demonstrates how we've successfully integrated Neo4j with Claude via MCP (Model Context Protocol), eliminating the steep learning curve of Cypher query language. Users can now query complex graph databases using plain English.

## What is MCP?

MCP (Model Context Protocol) is Anthropic's open standard for connecting AI assistants to external data sources. By connecting Neo4j to Claude, we've created a bridge that translates natural language into complex graph queries automatically.

## Resources

- **Official Neo4j MCP Server**: [github.com/neo4j-contrib/mcp-neo4j](https://github.com/neo4j-contrib/mcp-neo4j?tab=readme-ov-file)
- **Neo4j Cypher MCP Implementation**: [github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-cypher](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-cypher)
- **Video Demonstrations**: [youtube.com/@jasonkoo_dev](https://www.youtube.com/@jasonkoo_dev)

## Setup Instructions

### 1. Prerequisites

- Neo4j database running (e.g., via Docker)
- Claude Desktop installed
- Python with `uv` package manager

### 2. Install uv (if not already installed)

```bash
pip install uv
```

### 3. Configure Claude Desktop

Edit your Claude configuration file:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the Neo4j MCP server configuration:

```json
{
  "mcpServers": {
    "neo4j": {
      "command": "uvx",
      "args": ["mcp-neo4j-cypher@0.2.2", "--transport", "stdio"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "your-password",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

The Neo4j MCP server will now be available in your Claude conversations.

## Natural Language Query Examples

Here are examples of plain English queries that Claude can execute against your Neo4j database:

### 1. "What's the schema of my surveillance database?"

**What Claude does behind the scenes:**

- Automatically retrieves the complete graph schema
- Presents nodes, relationships, and properties in a readable format
- No need to remember Cypher schema commands

**Result**: Complete overview of your Person, Session, Phone, Email, Device, and Content nodes with all their relationships.

### 2. "Find sessions related to travel"

**What Claude does behind the scenes:**

```cypher
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE toLower(c.text) CONTAINS 'travel' 
   OR toLower(c.text) CONTAINS 'trip' 
   OR toLower(c.text) CONTAINS 'flight' 
   OR toLower(c.text) CONTAINS 'hotel'
RETURN s.sessionguid, s.starttime, s.targetname, s.subject, 
       LEFT(c.text, 150) AS content_preview
```

**Result**: Found Bangkok trip planning for February 16-23, 2022, including flight bookings (Denver to Bangkok) and travel arrangements.

### 3. "Show me all Person nodes in the database"

**What Claude does behind the scenes:**

- Queries all Person nodes
- Automatically handles pagination
- Returns formatted results

**Result**: List of 40 individuals including real people, companies, and system entities.

### 4. "Run a query to find the most connected people"

**What Claude does behind the scenes:**

```cypher
MATCH (p:Person)-[r]-()
WITH p, count(r) as connection_count
RETURN p.name as person, connection_count
ORDER BY connection_count DESC
```

**Result**: Ranked list showing Richard Eagle and Fred Merlin as the most connected with 5 connections each.

## Additional Natural Language Queries You Can Use

### Investigation Queries

- "Who has been in contact with Fred Merlin?"
- "Show me all email communications about meetings"
- "Find phone calls longer than 10 minutes"
- "Which devices are associated with multiple people?"
- "Show me sessions that happened last week"

### Pattern Detection

- "Find people who only communicate at night"
- "Show me clusters of people who frequently communicate with each other"
- "Identify phones that have been used by multiple people"
- "Find suspicious communication patterns"

### Relationship Analysis

- "How many degrees of separation between William Eagle and Kenzie Hawk?"
- "Show me the shortest path between two people"
- "Find common contacts between suspicious individuals"
- "Who acts as a communication hub in the network?"

### Content Search

- "Find all mentions of money transfers"
- "Search for discussions about specific locations"
- "Find encrypted or suspicious content"
- "Show me all sessions with attachments"

## Benefits of MCP Integration

1. **Zero Learning Curve**: No need to learn Cypher query language
2. **Natural Language**: Ask questions as you would to a colleague
3. **Intelligent Translation**: Claude understands context and intent
4. **Error Prevention**: No syntax errors or typos in queries
5. **Exploratory Analysis**: Discover insights through conversation

## Security Note

The MCP server requires explicit permission for each query execution, ensuring:

- Full control over what queries are run
- Audit trail of all database access
- No unauthorized data modifications

## Conclusion

This MCP integration transforms Neo4j from a tool requiring specialized knowledge into an accessible platform that anyone can query using natural language. It's particularly powerful for:

- Law enforcement investigators who need quick answers
- Analysts who want to explore data without technical barriers  
- Decision makers who need insights without learning query languages
- "Anyone who thinks in questions rather than code"

The combination of Neo4j's powerful graph database capabilities with Claude's natural language understanding creates a new paradigm for data exploration and analysis.