#!/usr/bin/env python3
"""
Export Neo4j database state (schema and content) for comparison between containers.

This script exports:
1. Schema information (labels, relationships, properties, indexes, constraints)
2. Node and relationship counts by type
3. Sample data for each label
4. Full property lists for each node/relationship type

Usage:
    python export-neo4j-state.py [--case CASE_NAME]
    
Output:
    data/{case_name}/neo4j-export-{timestamp}.json
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from neo4j import GraphDatabase
from collections import defaultdict

# Connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Sup3rSecur3!"


class Neo4jExporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def export_schema(self):
        """Export comprehensive schema information."""
        with self.driver.session() as session:
            schema = {
                "labels": self._get_labels(session),
                "relationships": self._get_relationships(session),
                "indexes": self._get_indexes(session),
                "constraints": self._get_constraints(session),
                "node_counts": self._get_node_counts(session),
                "relationship_counts": self._get_relationship_counts(session),
                "property_stats": self._get_property_stats(session),
                "sample_data": self._get_sample_data(session)
            }
            return schema

    def _get_labels(self, session):
        """Get all node labels."""
        result = session.run("CALL db.labels() YIELD label RETURN label ORDER BY label")
        return [record["label"] for record in result]

    def _get_relationships(self, session):
        """Get all relationship types."""
        result = session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType ORDER BY relationshipType")
        return [record["relationshipType"] for record in result]

    def _get_indexes(self, session):
        """Get all indexes with details."""
        result = session.run("""
            SHOW INDEXES 
            YIELD name, type, entityType, labelsOrTypes, properties, options
            RETURN name, type, entityType, labelsOrTypes, properties, options
            ORDER BY name
        """)
        return [dict(record) for record in result]

    def _get_constraints(self, session):
        """Get all constraints."""
        result = session.run("""
            SHOW CONSTRAINTS 
            YIELD name, type, entityType, labelsOrTypes, properties
            RETURN name, type, entityType, labelsOrTypes, properties
            ORDER BY name
        """)
        return [dict(record) for record in result]

    def _get_node_counts(self, session):
        """Get node counts by label."""
        counts = {}
        for label in self._get_labels(session):
            result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
            counts[label] = result.single()["count"]
        return counts

    def _get_relationship_counts(self, session):
        """Get relationship counts by type."""
        result = session.run("""
            MATCH ()-[r]->()
            RETURN type(r) as type, count(r) as count
            ORDER BY count DESC
        """)
        return {record["type"]: record["count"] for record in result}

    def _get_property_stats(self, session):
        """Get property statistics for each label."""
        stats = {"nodes": {}, "relationships": {}}
        
        # Node properties
        for label in self._get_labels(session):
            result = session.run(f"""
                MATCH (n:{label})
                UNWIND keys(n) as key
                RETURN key, count(DISTINCT n) as node_count
                ORDER BY key
            """)
            props = {}
            for record in result:
                props[record["key"]] = record["node_count"]
            if props:
                stats["nodes"][label] = props
        
        # Relationship properties
        for rel_type in self._get_relationships(session):
            result = session.run(f"""
                MATCH ()-[r:{rel_type}]->()
                WHERE keys(r) <> []
                UNWIND keys(r) as key
                RETURN key, count(DISTINCT r) as rel_count
                ORDER BY key
            """)
            props = {}
            for record in result:
                props[record["key"]] = record["rel_count"]
            if props:
                stats["relationships"][rel_type] = props
        
        return stats

    def _get_sample_data(self, session, limit=5):
        """Get sample data for each label."""
        samples = {}
        
        for label in self._get_labels(session):
            result = session.run(f"""
                MATCH (n:{label})
                RETURN properties(n) as props
                LIMIT {limit}
            """)
            samples[label] = [dict(record["props"]) for record in result]
        
        return samples

    def export_full_state(self, output_path):
        """Export complete database state to JSON file."""
        print("Exporting Neo4j database state...")
        
        state = {
            "export_timestamp": datetime.now().isoformat(),
            "database_info": {
                "uri": NEO4J_URI,
                "user": NEO4J_USER
            },
            "schema": self.export_schema()
        }
        
        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(state, f, indent=2, default=str)
        
        print(f"Export complete: {output_path}")
        return state


def main():
    parser = argparse.ArgumentParser(description="Export Neo4j database state")
    parser.add_argument("--case", default="default", help="Case name (default: 'default')")
    args = parser.parse_args()

    # Determine output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"data/{args.case}/neo4j-export-{timestamp}.json")

    # Export
    exporter = Neo4jExporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        state = exporter.export_full_state(output_path)
        
        # Print summary
        print("\nExport Summary:")
        print(f"- Labels: {len(state['schema']['labels'])}")
        print(f"- Relationships: {len(state['schema']['relationships'])}")
        print(f"- Indexes: {len(state['schema']['indexes'])}")
        print(f"- Total nodes: {sum(state['schema']['node_counts'].values())}")
        
    finally:
        exporter.close()


if __name__ == "__main__":
    main()