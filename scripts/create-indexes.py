#!/usr/bin/env python3
"""
Create missing indexes in Neo4j to match neo4j-sessions container.

This script creates all the performance and full-text indexes that were
present in the original neo4j-sessions container.
"""

import os
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Sup3rSecur3!"

# Get container name from environment
NEO_NAME = os.getenv("NEO_NAME", "neo4j-default")


def create_indexes(driver):
    """Create all missing indexes."""
    
    indexes_to_create = [
        # Full-text indexes
        ("CREATE FULLTEXT INDEX AliasText IF NOT EXISTS FOR (n:Alias) ON EACH [n.text]", "AliasText"),
        ("CREATE FULLTEXT INDEX ContentFullText IF NOT EXISTS FOR (n:Content) ON EACH [n.text]", "ContentFullText"),
        
        # Performance indexes
        ("CREATE INDEX phone_number_index IF NOT EXISTS FOR (p:Phone) ON (p.phone_number)", "phone_number_index"),
        ("CREATE INDEX email_address_index IF NOT EXISTS FOR (e:Email) ON (e.email_address)", "email_address_index"),
        ("CREATE INDEX session_guid_index IF NOT EXISTS FOR (s:Session) ON (s.session_guid)", "session_guid_index"),
        ("CREATE INDEX session_timestamp_index IF NOT EXISTS FOR (s:Session) ON (s.timestamp)", "session_timestamp_index"),
        ("CREATE INDEX person_name_index IF NOT EXISTS FOR (p:Person) ON (p.name)", "person_name_index"),
        ("CREATE INDEX device_id_index IF NOT EXISTS FOR (d:Device) ON (d.device_id)", "device_id_index"),
        ("CREATE INDEX device_guid_index IF NOT EXISTS FOR (d:Device) ON (d.guid)", "device_guid_index"),
        ("CREATE INDEX content_text_index IF NOT EXISTS FOR (c:Content) ON (c.text)", "content_text_index"),
        ("CREATE INDEX alias_text_index IF NOT EXISTS FOR (a:Alias) ON (a.text)", "alias_text_index"),
    ]
    
    with driver.session() as session:
        print(f"Creating indexes in {NEO_NAME} container...")
        
        for query, index_name in indexes_to_create:
            try:
                session.run(query)
                print(f"✓ Created index: {index_name}")
            except Exception as e:
                print(f"✗ Failed to create {index_name}: {str(e)}")
        
        # Show final index count
        result = session.run("SHOW INDEXES YIELD name RETURN count(*) as total")
        total = result.single()["total"]
        print(f"\nTotal indexes in database: {total}")


def verify_genai_plugin(driver):
    """Verify Neo4j GenAI plugin is available."""
    
    with driver.session() as session:
        try:
            # Test if GenAI functions are available
            result = session.run("""
                SHOW FUNCTIONS 
                YIELD name 
                WHERE name STARTS WITH 'genai.' 
                RETURN collect(name) as genai_functions
            """)
            functions = result.single()["genai_functions"]
            
            if functions:
                print(f"\nGenAI plugin is available with {len(functions)} functions:")
                for func in sorted(functions)[:5]:  # Show first 5
                    print(f"  - {func}")
                if len(functions) > 5:
                    print(f"  ... and {len(functions) - 5} more")
                
                # Check for vector encoding functions specifically
                vector_funcs = [f for f in functions if 'vector.encode' in f]
                if vector_funcs:
                    print(f"\nVector encoding functions available:")
                    for func in vector_funcs:
                        print(f"  - {func}")
            else:
                print("\n⚠️  GenAI plugin not found. Container may need to be restarted with GenAI enabled.")
                
        except Exception as e:
            print(f"\n⚠️  Error checking GenAI plugin: {str(e)}")


def check_embeddings_status(driver):
    """Check current embedding status."""
    
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Content)
            RETURN 
                count(c) as total,
                count(c.text) as with_text,
                count(c.embedding) as with_embedding,
                count(CASE WHEN size(c.embedding) = 1536 THEN 1 END) as embedding_1536
        """)
        stats = result.single()
        
        print(f"\nEmbedding status in {NEO_NAME}:")
        print(f"  Total Content nodes: {stats['total']}")
        print(f"  Nodes with text: {stats['with_text']}")
        print(f"  Nodes with embeddings: {stats['with_embedding']}")
        print(f"  1536-dim embeddings: {stats['embedding_1536']}")


def main():
    print(f"Connecting to {NEO_NAME} container...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        # Check GenAI plugin availability
        verify_genai_plugin(driver)
        
        # Check embedding status
        check_embeddings_status(driver)
        
        # Create indexes
        create_indexes(driver)
        
    finally:
        driver.close()


if __name__ == "__main__":
    main()