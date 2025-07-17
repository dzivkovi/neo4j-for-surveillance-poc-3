"""
Parser for EVAL-NN.md files - extracts Cypher queries and expected results.
Supports both AST parsing (robust) and regex fallback for edge cases.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Try to use mistune for robust parsing, fallback to regex if not available
try:
    import mistune

    USE_AST = True
except ImportError:
    USE_AST = False


@dataclass
class EvalTestCase:
    """Represents a single test case from an EVAL file"""

    id: str  # e.g., "EVAL-02"
    file_path: Path  # Full path to source file
    query: str  # Cypher query text
    expected_result: dict  # Parsed expected values
    metadata: dict  # Category, Duration-ms, etc.


def parse_eval_files(directory: Path) -> list[EvalTestCase]:
    """
    Parse all EVAL-NN.md files in directory and extract test cases.

    Args:
        directory: Path to evals/passed/ directory

    Returns:
        List of EvalTestCase objects ready for pytest
    """
    test_cases = []

    # Sort for consistent test ordering
    for file_path in sorted(directory.glob("EVAL-*.md")):
        try:
            case = extract_test_case(file_path)
            if case:
                test_cases.append(case)
        except Exception as e:
            # Log but don't fail - defensive programming
            print(f"Warning: Failed to parse {file_path}: {e}")

    return test_cases


def extract_test_case(file_path: Path) -> Optional[EvalTestCase]:
    """Extract single test case from EVAL file"""
    content = file_path.read_text(encoding="utf-8")

    # Extract components
    query = extract_cypher_query(content)
    if not query:
        return None

    expected = extract_expected_result(content)
    metadata = extract_metadata(content)

    return EvalTestCase(
        id=file_path.stem, file_path=file_path, query=query, expected_result=expected, metadata=metadata
    )


def extract_cypher_query(content: str) -> Optional[str]:
    """Extract Cypher query using AST or regex fallback"""
    if USE_AST:
        # Use mistune AST parsing (more robust)
        md = mistune.create_markdown(renderer="ast")
        ast = md(content)

        in_query_section = False
        for node in ast:
            # Check for ### Query heading
            if node.get("type") == "heading" and node.get("level") == 3:
                heading_text = extract_text_from_ast(node)
                in_query_section = "query" in heading_text.lower()

            # Extract cypher code block
            elif in_query_section and node.get("type") == "code_block":
                if node.get("info", "").lower() == "cypher":
                    return node.get("raw", "").strip()

    # Fallback to regex (handles edge cases)
    pattern = r"### Query\s*```cypher\s*(.*?)\s*```"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if match:
        query = match.group(1).strip()
        # Also check for inline expected values
        query = extract_inline_expected(query)
        return query

    return None


def extract_text_from_ast(node: dict) -> str:
    """Helper to extract text from AST node"""
    if node.get("type") == "text":
        return node.get("raw", "")

    text_parts = []
    for child in node.get("children", []):
        if isinstance(child, dict):
            text_parts.append(extract_text_from_ast(child))

    return " ".join(text_parts).strip()


def extract_inline_expected(query: str) -> str:
    """Extract and process inline -- expected: comments"""
    # Store expected values found in comments
    expected_pattern = r"--\s*expected:\s*(.+)$"
    matches = re.findall(expected_pattern, query, re.MULTILINE)

    if matches:
        # Store in global for later processing (hacky but works)
        global _inline_expected
        _inline_expected = matches[0].strip()

    # Return query without comments
    return re.sub(expected_pattern, "", query, flags=re.MULTILINE).strip()


def extract_expected_result(content: str) -> dict:
    """
    Extract expected results from ### Actual Result section.
    Handles various formats found in EVAL files.
    """
    result = {}

    # Check for inline expected first
    if hasattr(extract_inline_expected, "_inline_expected"):
        inline = getattr(extract_inline_expected, "_inline_expected", None)
        if inline:
            result["inline"] = inline
            delattr(extract_inline_expected, "_inline_expected")

    # Pattern for ### Actual Result section
    pattern = r"### Actual Result\s*```\s*(.*?)\s*```"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return result

    result_text = match.group(1).strip()

    # Parse different result formats
    # Format 1: field_name: value
    for line in result_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Try to parse numeric values
            if value.replace(".", "", 1).replace("-", "", 1).isdigit():
                if "." in value:
                    result[key] = float(value)
                else:
                    result[key] = int(value)
            else:
                result[key] = value

    # Common aliases for count fields
    count_fields = ["discussions_voyage", "shed_sessions", "travel_discussions", "session_count", "count", "total"]
    score_fields = ["meilleur_score", "relevance_score", "max_score", "score"]

    # Normalize to standard keys
    for field in count_fields:
        if field in result:
            result["count"] = result[field]
            break

    for field in score_fields:
        if field in result:
            result["score"] = result[field]
            break

    return result


def extract_metadata(content: str) -> dict:
    """Extract metadata from EVAL file header"""
    metadata = {}

    # Parse header metadata (first 20 lines)
    lines = content.split("\n")[:20]

    for line in lines:
        if line.startswith("Category:"):
            metadata["Category"] = line.split(":", 1)[1].strip()
        elif line.startswith("Duration-ms:"):
            value = line.split(":", 1)[1].strip()
            if value != "—" and value.isdigit():
                metadata["Duration-ms"] = int(value)
        elif line.startswith("Status:"):
            metadata["Status"] = line.split(":", 1)[1].strip()
        elif line.startswith("Added:"):
            metadata["Added"] = line.split(":", 1)[1].strip()

    return metadata


# Example usage for testing parser independently
if __name__ == "__main__":
    from pathlib import Path

    evals_dir = Path("evals/passed")
    cases = parse_eval_files(evals_dir)
    print(f"Found {len(cases)} test cases")
    for case in cases[:3]:
        print(f"\n{case.id}:")
        print(f"  Query: {case.query[:50]}...")
        print(f"  Expected: {case.expected_result}")
        print(f"  Category: {case.metadata.get('Category', 'Unknown')}")
