#!/usr/bin/env python3
"""
Decode SMS content from base64 and create Content nodes for search
Priority: Speed of delivery - decode SMS messages immediately
"""

import base64
import json
import os
from neo4j import GraphDatabase
import datetime
from typing import Optional

# Database connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Sup3rSecur3!"

# Get dataset from environment (for dataset awareness)
DATASET = os.getenv('DATASET', 'default')
print(f"Working with dataset: {DATASET}")

def decode_base64_content(content: str) -> Optional[str]:
    """Decode base64 content, handle potential errors"""
    try:
        if not content:
            return None
        decoded_bytes = base64.b64decode(content)
        decoded_text = decoded_bytes.decode('utf-8', errors='ignore')
        return decoded_text.strip()
    except Exception as e:
        print(f"Error decoding content: {e}")
        return None

def test_decode_samples():
    """Test decoding the sample SMS content we found"""
    samples = [
        "Gl0IG1lIGFzYXAKCg==",
        "W9vb29vbwoK",
        "VQmVCBGcmVlIE1zZzogQXV0byBSZWZpbGwgaXMgdGhlIGVhc3kgd2F5IHRvIGtlZXAgeW91ciBHb1Bob25lIGFjY291bnQgcmVhZHkgdG8gZ28hIEdvIHRvIG15cHJlcGFpZHJlZmlsbC5jb20gb3IgKjcyOSB0byBzaWduIHVwLiBSZXBseSBTVE9QIHRvIGVuZCBta"
    ]
    
    for i, sample in enumerate(samples):
        decoded = decode_base64_content(sample)
        print(f"Sample {i+1}: {decoded}")

def create_content_nodes_for_sms():
    """Create Content nodes for all SMS sessions with decoded text"""
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            # Get all SMS sessions with previewcontent
            query = """
            MATCH (s:Session {sessiontype: "Messaging", contenttype: "SMS"})
            WHERE s.previewcontent IS NOT NULL
            RETURN s.sessionguid as session_id, s.previewcontent as content, s.sessiondate as date
            """
            
            result = session.run(query)
            sms_sessions = list(result)
            
            print(f"Found {len(sms_sessions)} SMS sessions to process")
            
            processed = 0
            created = 0
            
            for record in sms_sessions:
                session_id = record["session_id"]
                base64_content = record["content"]
                session_date = record["date"]
                
                # Decode the SMS content
                decoded_text = decode_base64_content(base64_content)
                
                if decoded_text and len(decoded_text.strip()) > 0:
                    # Create Content node
                    create_query = """
                    MATCH (s:Session {sessionguid: $session_id})
                    CREATE (c:Content {
                        text: $text,
                        session_id: $session_id,
                        created_at: datetime(),
                        source: "sms_extraction"
                    })
                    CREATE (s)-[:HAS_CONTENT]->(c)
                    RETURN c.text as created_text
                    """
                    
                    session.run(create_query, {
                        "session_id": session_id,
                        "text": decoded_text
                    })
                    
                    created += 1
                    
                    if created % 100 == 0:
                        print(f"Created {created} Content nodes...")
                
                processed += 1
            
            print(f"Processing complete:")
            print(f"- Processed: {processed} SMS sessions")
            print(f"- Created: {created} Content nodes")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    print("Testing SMS content decoding...")
    test_decode_samples()
    print("\nExtracting SMS content...")
    create_content_nodes_for_sms()