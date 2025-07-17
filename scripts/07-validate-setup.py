#!/usr/bin/env python3
"""
Validate complete Neo4j surveillance database setup.

This script verifies that all constraints, indexes, and data are properly configured.
It performs both core validations (required for any dataset) and optional checks
that can be customized based on your specific use case.

Prerequisites:
  1. Neo4j container running
  2. Schema created (scripts/01-create-schema.sh)
  3. Sessions imported (02-import-sessions.py)
  4. Content extracted (03-decode-sms-content.py, 04-import-additional-content.py)
  5. Transcripts imported (05-import-transcripts.py)
  6. Embeddings generated (06-generate-embeddings.sh)

Usage:
    python scripts/07-validate-setup.py

Customization:
    Look for "OPTIONAL VALIDATIONS" sections to enable dataset-specific checks.
"""

import os
from neo4j import GraphDatabase
from collections import defaultdict

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Sup3rSecur3!"
NEO_NAME = os.getenv("NEO_NAME", "neo4j-default")

# ================== CUSTOMIZATION GUIDE ==================
# This validation script is designed to work with any surveillance dataset.
# 
# Core validations (always run):
# - Schema constraints and indexes
# - Basic node type presence
# - Embedding completeness
# - Relationship integrity
#
# Optional validations (uncomment as needed):
# - Session type distribution
# - Communication patterns
# - Content extraction verification
# - Dataset-specific business rules
#
# To customize for your dataset:
# 1. Keep core validations unchanged
# 2. Uncomment relevant optional sections
# 3. Add dataset-specific checks at the end
# =========================================================

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
    warnings = []  # Non-critical issues
    
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
                # Some node types are optional depending on dataset
                if node_type in ["Session", "Person", "Phone"]:
                    issues.append(f"No {node_type} nodes found")
                else:
                    warnings.append(f"No {node_type} nodes (may be normal for this dataset)")
        
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
        
        if stats["total"] == 0:
            print("   ⚠ No Content nodes found (normal for minimal test datasets)")
            warnings.append("No Content nodes - expected for basic test data")
        elif stats["with_embedding"] == stats["with_text"] and stats["with_text"] > 0:
            print(f"   ✓ All {stats['with_text']} Content nodes with text have embeddings")
        else:
            print(f"   ✗ Only {stats['with_embedding']}/{stats['with_text']} Content nodes have embeddings")
            if stats["with_text"] > stats["with_embedding"]:
                issues.append(f"{stats['with_text'] - stats['with_embedding']} Content nodes missing embeddings")
        
        if stats["with_embedding"] > 0:
            if stats["correct_dims"] == stats["with_embedding"]:
                print(f"   ✓ All embeddings have correct dimensions (1536)")
            else:
                print(f"   ✗ Some embeddings have wrong dimensions")
                issues.append("Some embeddings have incorrect dimensions")
        
        # Basic Content validation
        print("\n5. Checking Content Sources...")
        result = session.run("""
            MATCH (c:Content)
            WHERE c.source IS NOT NULL
            RETURN c.source as source, count(*) as count
            ORDER BY count DESC
        """)
        
        content_sources = {r["source"]: r["count"] for r in result}
        if content_sources:
            print("   Content by source:")
            for source, count in content_sources.items():
                print(f"   ✓ {source}: {count} nodes")
        else:
            print("   ⚠ No Content nodes with source field (check import process)")
        
        # Relationship integrity
        print("\n6. Checking Relationship Integrity...")
        
        # Sessions should have participants
        result = session.run("""
            MATCH (s:Session)
            WITH s, COUNT { (s)<-[:PARTICIPATED_IN]-() } as participants
            RETURN 
                count(s) as total_sessions,
                count(CASE WHEN participants > 0 THEN 1 END) as with_participants,
                avg(participants) as avg_participants
        """)
        rel_stats = result.single()
        
        if rel_stats["with_participants"] == rel_stats["total_sessions"]:
            print(f"   ✓ All {rel_stats['total_sessions']} sessions have participants")
        else:
            orphaned = rel_stats["total_sessions"] - rel_stats["with_participants"]
            print(f"   ⚠ {orphaned} sessions without participants")
            warnings.append(f"{orphaned} orphaned sessions")
        
        # ================== OPTIONAL VALIDATIONS ==================
        # Uncomment the following sections based on your dataset needs
        
        # # OPTIONAL: Check for specific session types
        # print("\n7. [OPTIONAL] Checking Session Types...")
        # result = session.run("""
        #     MATCH (s:Session)
        #     RETURN s.sessiontype as type, count(*) as count
        #     ORDER BY count DESC
        # """)
        # session_types = {r["type"]: r["count"] for r in result}
        # for stype, count in session_types.items():
        #     print(f"   - {stype}: {count} sessions")
        
        # # OPTIONAL: Validate communication patterns
        # print("\n8. [OPTIONAL] Checking Communication Patterns...")
        # result = session.run("""
        #     MATCH (p:Phone)-[:PARTICIPATED_IN]->(s:Session)
        #     WITH p, 
        #          count(CASE WHEN s.sessiontype = 'Telephony' THEN 1 END) as calls,
        #          count(CASE WHEN s.sessiontype = 'Messaging' THEN 1 END) as messages
        #     WHERE calls > 0 OR messages > 0
        #     RETURN count(*) as phones_with_activity,
        #            count(CASE WHEN calls > 0 AND messages > 0 THEN 1 END) as phones_with_both
        # """)
        # comm_stats = result.single()
        # if comm_stats:
        #     print(f"   - Phones with activity: {comm_stats['phones_with_activity']}")
        #     print(f"   - Phones with both calls and messages: {comm_stats['phones_with_both']}")
        
        # # OPTIONAL: Check for extracted content patterns
        # print("\n9. [OPTIONAL] Checking Extracted Content...")
        # result = session.run("""
        #     MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
        #     RETURN s.sessiontype as session_type, 
        #            count(distinct s) as sessions_with_content,
        #            count(c) as content_nodes
        #     ORDER BY sessions_with_content DESC
        # """)
        # for record in result:
        #     print(f"   - {record['session_type']}: {record['sessions_with_content']} sessions → {record['content_nodes']} content")
        
        # =========================================================
    
    # Summary
    print("\n" + "=" * 60)
    
    if warnings and not issues:
        print(f"✅ Core validation passed with {len(warnings)} warnings:")
        for warning in warnings:
            print(f"   ⚠ {warning}")
        print("\n   These warnings are typically OK for test datasets.")
    elif not issues:
        print("✅ All checks passed! Setup is complete.")
    else:
        print(f"❌ Found {len(issues)} critical issues:")
        for issue in issues:
            print(f"   - {issue}")
        if warnings:
            print(f"\n⚠ Also found {len(warnings)} warnings:")
            for warning in warnings:
                print(f"   - {warning}")
        
        print("\nTo fix critical issues:")
        print("1. Ensure schema is created: ./scripts/01-create-schema.sh")
        print("2. Import all data: 02-import-sessions.py → 03-decode-sms-content.py → 04-import-additional-content.py")
        print("3. If embeddings are missing: export OPENAI_API_KEY='sk-...' && ./scripts/06-generate-embeddings.sh")
    
    print("\n💡 Tip: Uncomment OPTIONAL VALIDATIONS in this script for dataset-specific checks.")
    
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