#!/bin/bash

# Step 6: Apply Analyst Knowledge Aliases (MANUAL)
# This script applies investigation-specific name variations discovered through analysis
# Execute ONLY after completing steps 1-5 of the setup process

set -e

# Check if NEO_NAME is set
if [ -z "$NEO_NAME" ]; then
    echo "❌ NEO_NAME environment variable not set"
    echo "Set it with: export NEO_NAME=\"neo4j-tmp\" (or your container name)"
    exit 1
fi

# Check if container is running
if ! docker ps | grep -q "$NEO_NAME"; then
    echo "❌ Container $NEO_NAME is not running"
    echo "Start it with: ./run_neo4j.sh <case_name>"
    exit 1
fi

# Check if analyst aliases file exists
ALIASES_FILE="scripts/cypher/06-analyst-aliases-template.cypher"
if [ ! -f "$ALIASES_FILE" ]; then
    echo "❌ Analyst aliases template not found: $ALIASES_FILE"
    echo "Template file should exist in scripts/cypher/ directory"
    exit 1
fi

echo "🔧 Applying analyst knowledge aliases (template for demonstration)"
echo "📁 Reading from: $ALIASES_FILE"
echo "🎯 Target container: $NEO_NAME"
echo "⚠️  In production, customize this file with case-specific aliases"
echo

# Apply aliases
echo "Executing analyst aliases..."
docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3! < "$ALIASES_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Analyst aliases applied successfully"
    echo
    echo "📊 Checking alias count..."
    echo "MATCH (a:Alias) RETURN count(a) AS total_aliases;" | docker exec -i "$NEO_NAME" cypher-shell -u neo4j -p Sup3rSecur3!
else
    echo "❌ Failed to apply analyst aliases"
    exit 1
fi