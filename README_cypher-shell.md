# Running Cypher Queries in Neo4j Docker Container

## Method 1: Execute cypher-shell inside the container

```bash
# Basic syntax
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3!

# Run a single query
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! "MATCH (n) RETURN count(n);"

# Run a query file
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < queries/investigative.cypher

# Run with formatted output
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! --format plain "MATCH (s:Session) RETURN keys(s) LIMIT 1;"
```

## Method 2: Interactive shell session

```bash
# Start an interactive cypher-shell session
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3!

# Once inside, you can run queries:
neo4j@neo4j> MATCH (n) RETURN count(n);
neo4j@neo4j> :exit
```

## Method 3: Using bash heredoc for multi-line queries

```bash
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! --format plain <<'EOF'
MATCH (s:Session)
RETURN keys(s) as properties
LIMIT 1;
EOF
```

## Method 4: Copy and execute files

```bash
# Copy a query file into the container first
docker cp queries/practical-investigation-queries.cypher neo4j-sessions:/tmp/

# Then execute it
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! -f /tmp/practical-investigation-queries.cypher
```

## Useful Options

- `--format plain` - Plain text output (no boxes)
- `--format json` - JSON output
- `--format verbose` - Detailed output with execution plans
- `-f filename` - Execute queries from a file
- `--non-interactive` - Don't prompt for input

## Example: Check Session Properties

```bash
# Let's check what properties Session nodes actually have
docker exec -it neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! --format plain "MATCH (s:Session) RETURN DISTINCT keys(s) as properties LIMIT 5;"
```
