#!/usr/bin/env python3
"""
Step 5: Validate complete Neo4j setup.

This script verifies that all constraints, indexes, and data are properly configured.
It checks the complete setup from schema through embeddings to ensure everything
is working correctly.

Prerequisites:
  1. Neo4j container running
  2. Schema created (scripts/01-create-schema.sh)
  3. Sessions imported (02-import-sessions.py)
  4. Transcripts imported (03-import-transcripts.py)
  5. Embeddings generated (04-generate-embeddings.cypher)

Usage:
    python scripts/python/05-validate-setup.py
"""

import os
from neo4j import GraphDatabase
from collections import defaultdict

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Sup3rSecur3!"
NEO_NAME = os.getenv("NEO_NAME", "neo4j-default")

# Expected configuration based on original neo4j-sessions
EXPECTED_CONSTRAINTS = {
    "session_guid": ("Session", "sessionguid"),
    "phone_number": ("Phone", "number"),
    "email_addr": ("Email", "email"),
    "device_imei": ("Device", "imei"),
    "alias_raw_unique": ("Alias", "rawValue"),
}

EXPECTED_INDEXES = {
    # Full-text indexes
    "ContentFullText": ("FULLTEXT", ["Content"], ["text"]),
    "AliasText": ("FULLTEXT", ["Alias"], ["rawValue"]),
    
    # Vector index
    "ContentVectorIndex": ("VECTOR", ["Content"], ["embedding"]),
    
    # Spatial index
    "locationGeo": ("POINT", ["Location"], ["geo"]),
    
    # Range indexes
    "sessionDuration": ("RANGE", ["Session"], ["durationinseconds"]),
    "session_createddate": ("RANGE", ["Session"], ["createddate"]),
    "session_sessiontype": ("RANGE", ["Session"], ["sessiontype"]),
    "person_name_index": ("RANGE", ["Person"], ["name"]),  # Note: index name has _index suffix
}

EXPECTED_NODE_TYPES = ["Session", "Person", "Phone", "Email", "Device", "Location", "Content", "Alias"]


def verify_setup(driver):
    """Run all verification checks."""
    print(f"Verifying Neo4j setup for {NEO_NAME}...")
    print("=" * 60)
    
    issues = []
    
    with driver.session() as session:
        # Check constraints
        print("\n1. Checking Constraints...")
        result = session.run("SHOW CONSTRAINTS")
        constraints = {r["name"]: (r["labelsOrTypes"][0], r["properties"][0]) for r in result}
        
        for name, (label, prop) in EXPECTED_CONSTRAINTS.items():
            if name in constraints:
                actual_label, actual_prop = constraints[name]
                if actual_label == label and actual_prop == prop:
                    print(f"   ✓ {name}: {label}.{prop}")
                else:
                    print(f"   ✗ {name}: Expected {label}.{prop}, got {actual_label}.{actual_prop}")
                    issues.append(f"Constraint {name} has wrong configuration")
            else:
                print(f"   ✗ {name}: MISSING")
                issues.append(f"Constraint {name} is missing")
        
        # Check indexes
        print("\n2. Checking Indexes...")
        result = session.run("SHOW INDEXES")
        indexes = {}
        for r in result:
            if r["name"] and not r["name"].startswith("index_"):  # Skip auto-generated names
                indexes[r["name"]] = (r["type"], r["labelsOrTypes"], r["properties"])
        
        for name, (idx_type, labels, props) in EXPECTED_INDEXES.items():
            if name in indexes:
                actual_type, actual_labels, actual_props = indexes[name]
                if actual_type == idx_type:
                    print(f"   ✓ {name}: {idx_type} on {labels[0]}.{props[0]}")
                else:
                    print(f"   ✗ {name}: Expected {idx_type}, got {actual_type}")
                    issues.append(f"Index {name} has wrong type")
            else:
                print(f"   ✗ {name}: MISSING")
                issues.append(f"Index {name} is missing")
        
        # Check node counts
        print("\n3. Checking Node Counts...")
        result = session.run("""
            MATCH (n)
            WITH labels(n)[0] as label, count(n) as count
            RETURN label, count
            ORDER BY label
        """)
        node_counts = {r["label"]: r["count"] for r in result}
        
        for node_type in EXPECTED_NODE_TYPES:
            count = node_counts.get(node_type, 0)
            if count > 0:
                print(f"   ✓ {node_type}: {count} nodes")
            else:
                print(f"   ⚠ {node_type}: No nodes found")
                if node_type != "Alias":  # Alias nodes are created during import
                    issues.append(f"No {node_type} nodes found")
        
        # Check embeddings
        print("\n4. Checking Embeddings...")
        result = session.run("""
            MATCH (c:Content)
            RETURN 
                count(c) as total,
                count(c.text) as with_text,
                count(c.embedding) as with_embedding,
                count(CASE WHEN size(c.embedding) = 1536 THEN 1 END) as correct_dims
        """)
        stats = result.single()
        
        if stats["with_embedding"] == stats["with_text"] and stats["with_text"] > 0:
            print(f"   ✓ All {stats['with_text']} Content nodes with text have embeddings")
        else:
            print(f"   ✗ Only {stats['with_embedding']}/{stats['with_text']} Content nodes have embeddings")
            if stats["with_text"] > stats["with_embedding"]:
                issues.append(f"{stats['with_text'] - stats['with_embedding']} Content nodes missing embeddings")
        
        if stats["correct_dims"] == stats["with_embedding"] and stats["with_embedding"] > 0:
            print(f"   ✓ All embeddings have correct dimensions (1536)")
        else:
            print(f"   ✗ Some embeddings have wrong dimensions")
            issues.append("Some embeddings have incorrect dimensions")
    
    # Summary
    print("\n" + "=" * 60)
    if not issues:
        print("✅ All checks passed! Setup is complete.")
    else:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nTo fix:")
        print("1. Ensure schema is created: ./scripts/01-create-schema.sh")
        print("2. If embeddings are missing, run: ./scripts/04-generate-embeddings.sh")
    
    return len(issues) == 0


def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        success = verify_setup(driver)
        exit(0 if success else 1)
    finally:
        driver.close()


if __name__ == "__main__":
    main()