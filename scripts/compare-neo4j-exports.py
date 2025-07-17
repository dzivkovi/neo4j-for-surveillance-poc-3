#!/usr/bin/env python3
"""
Compare two Neo4j database exports to identify differences.

This script compares:
- Schema differences (labels, relationships, properties)
- Index and constraint differences
- Node/relationship count differences
- Property usage differences

Usage:
    python compare-neo4j-exports.py export1.json export2.json
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any


def load_export(filepath: Path) -> Dict[str, Any]:
    """Load a Neo4j export JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def compare_lists(list1: List[str], list2: List[str], name: str) -> None:
    """Compare two lists and print differences."""
    set1 = set(list1)
    set2 = set(list2)
    
    only_in_1 = set1 - set2
    only_in_2 = set2 - set1
    
    if only_in_1 or only_in_2:
        print(f"\n{name} Differences:")
        if only_in_1:
            print(f"  Only in first:  {sorted(only_in_1)}")
        if only_in_2:
            print(f"  Only in second: {sorted(only_in_2)}")
    else:
        print(f"\n{name}: ✓ Identical")


def compare_counts(counts1: Dict[str, int], counts2: Dict[str, int], name: str) -> None:
    """Compare count dictionaries."""
    all_keys = set(counts1.keys()) | set(counts2.keys())
    
    differences = []
    for key in sorted(all_keys):
        count1 = counts1.get(key, 0)
        count2 = counts2.get(key, 0)
        if count1 != count2:
            differences.append(f"  {key}: {count1} → {count2} (diff: {count2 - count1:+d})")
    
    if differences:
        print(f"\n{name} Count Differences:")
        for diff in differences:
            print(diff)
    else:
        print(f"\n{name} Counts: ✓ Identical")


def compare_indexes(indexes1: List[Dict], indexes2: List[Dict]) -> None:
    """Compare index configurations."""
    def index_key(idx):
        return f"{idx['name']}_{idx['type']}_{str(idx['labelsOrTypes'])}"
    
    idx1_map = {index_key(idx): idx for idx in indexes1}
    idx2_map = {index_key(idx): idx for idx in indexes2}
    
    only_in_1 = set(idx1_map.keys()) - set(idx2_map.keys())
    only_in_2 = set(idx2_map.keys()) - set(idx1_map.keys())
    
    if only_in_1 or only_in_2:
        print("\nIndex Differences:")
        if only_in_1:
            print("  Only in first:")
            for key in sorted(only_in_1):
                idx = idx1_map[key]
                print(f"    - {idx['name']} ({idx['type']}) on {idx['labelsOrTypes']}")
        if only_in_2:
            print("  Only in second:")
            for key in sorted(only_in_2):
                idx = idx2_map[key]
                print(f"    - {idx['name']} ({idx['type']}) on {idx['labelsOrTypes']}")
    else:
        print("\nIndexes: ✓ Identical")


def compare_properties(props1: Dict, props2: Dict) -> None:
    """Compare property statistics."""
    print("\nProperty Usage Differences:")
    
    # Compare node properties
    all_labels = set(props1.get("nodes", {}).keys()) | set(props2.get("nodes", {}).keys())
    
    if all_labels:
        print("  Node Properties:")
        for label in sorted(all_labels):
            label_props1 = set(props1.get("nodes", {}).get(label, {}).keys())
            label_props2 = set(props2.get("nodes", {}).get(label, {}).keys())
            
            only_in_1 = label_props1 - label_props2
            only_in_2 = label_props2 - label_props1
            
            if only_in_1 or only_in_2:
                print(f"    {label}:")
                if only_in_1:
                    print(f"      Only in first:  {sorted(only_in_1)}")
                if only_in_2:
                    print(f"      Only in second: {sorted(only_in_2)}")
    
    # Compare relationship properties
    all_rels = set(props1.get("relationships", {}).keys()) | set(props2.get("relationships", {}).keys())
    
    if all_rels:
        print("  Relationship Properties:")
        for rel in sorted(all_rels):
            rel_props1 = set(props1.get("relationships", {}).get(rel, {}).keys())
            rel_props2 = set(props2.get("relationships", {}).get(rel, {}).keys())
            
            only_in_1 = rel_props1 - rel_props2
            only_in_2 = rel_props2 - rel_props1
            
            if only_in_1 or only_in_2:
                print(f"    {rel}:")
                if only_in_1:
                    print(f"      Only in first:  {sorted(only_in_1)}")
                if only_in_2:
                    print(f"      Only in second: {sorted(only_in_2)}")


def main():
    parser = argparse.ArgumentParser(description="Compare Neo4j database exports")
    parser.add_argument("export1", help="First export file")
    parser.add_argument("export2", help="Second export file")
    args = parser.parse_args()

    # Load exports
    export1 = load_export(Path(args.export1))
    export2 = load_export(Path(args.export2))
    
    print(f"Comparing Neo4j Exports:")
    print(f"  Export 1: {args.export1} ({export1['export_timestamp']})")
    print(f"  Export 2: {args.export2} ({export2['export_timestamp']})")
    print("=" * 60)
    
    schema1 = export1['schema']
    schema2 = export2['schema']
    
    # Compare basic schema elements
    compare_lists(schema1['labels'], schema2['labels'], "Labels")
    compare_lists(schema1['relationships'], schema2['relationships'], "Relationship Types")
    
    # Compare counts
    compare_counts(schema1['node_counts'], schema2['node_counts'], "Node")
    compare_counts(schema1['relationship_counts'], schema2['relationship_counts'], "Relationship")
    
    # Compare indexes
    compare_indexes(schema1['indexes'], schema2['indexes'])
    
    # Compare properties
    compare_properties(schema1['property_stats'], schema2['property_stats'])
    
    print("\n" + "=" * 60)
    print("Comparison complete!")


if __name__ == "__main__":
    main()