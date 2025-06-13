#!/bin/bash

# Generate Business Rules README
# Usage: ./generate-business-rules-readme.sh > docs/business-rules/README.md

RULES_DIR="docs/business-rules"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "# Business Rules Index"
echo ""
echo "Generated on $TIMESTAMP"
echo ""
echo "## Active Rules"
echo ""
echo "| Rule | Priority | Status | Date |"
echo "|------|----------|--------|------|"

# Count statistics
TOTAL=0
TODO=0
IN_PROGRESS=0
DONE=0
BLOCKED=0
CRITICAL=0
HIGH=0
MEDIUM=0
LOW=0

# Process each rule file and build table
for file in $RULES_DIR/*.md; do
    # Skip template and README
    if [[ $(basename "$file") == "_template.md" ]] || [[ $(basename "$file") == "README.md" ]]; then
        continue
    fi
    
    # Extract metadata (strip carriage returns)
    TITLE=$(head -n 1 "$file" | sed 's/# //' | tr -d '\r')
    STATUS=$(grep "^\*\*Status\*\*:" "$file" | awk -F': ' '{print $2}' | xargs | tr -d '\r')
    PRIORITY=$(grep "^\*\*Priority\*\*:" "$file" | awk -F': ' '{print $2}' | xargs | tr -d '\r')
    DATE=$(grep "^\*\*Date\*\*:" "$file" | awk -F': ' '{print $2}' | xargs | tr -d '\r')
    FILENAME=$(basename "$file")
    
    # Build table row
    echo "| [$TITLE]($FILENAME) | $PRIORITY | $STATUS | $DATE |"
    
    # Count statistics
    ((TOTAL++))
    
    case "$STATUS" in
        TODO) ((TODO++)) ;;
        IN-PROGRESS) ((IN_PROGRESS++)) ;;
        DONE) ((DONE++)) ;;
        BLOCKED) ((BLOCKED++)) ;;
    esac
    
    case "$PRIORITY" in
        Critical) ((CRITICAL++)) ;;
        High) ((HIGH++)) ;;
        Medium) ((MEDIUM++)) ;;
        Low) ((LOW++)) ;;
    esac
done

echo ""
echo "## Quick Stats"
echo "- **Total Rules**: $TOTAL"
echo "  - **Critical**: $CRITICAL"
echo "  - **High**: $HIGH"
echo "  - **Medium**: $MEDIUM"
echo "  - **Low**: $LOW"
echo ""
echo "- **Progress Status**:"
echo "  - **TODO**: $TODO"
echo "  - **In Progress**: $IN_PROGRESS"
echo "  - **Blocked**: $BLOCKED"
echo "  - **Implemented**: $DONE"
echo ""
echo "## Usage"
echo "1. Copy \`_template.md\` for new rules"
echo "2. Use descriptive filenames (kebab-case)"
echo "3. Use \`./scripts/bash/generate-business-rules-readme.sh\` to update this index when adding or editing business rule files"