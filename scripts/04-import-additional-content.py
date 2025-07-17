#!/usr/bin/env python3
"""
Ultra-simple script to import additional content types into Neo4j
Based on the clarity from ER diagram: just add new sessiontypes!

This imports:
- Police reports (fulltext[] from Intel Report sessions)
- Social media posts (fulltext[] from Social Network sessions)  
- Phone call transcripts (documents[].text from Telephony sessions)
- Document files (documents[].text from Generic File sessions)
"""

import json
import sys
from neo4j import GraphDatabase
from datetime import datetime
from typing import List, Dict, Optional
import os

# Database connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Sup3rSecur3!"

def get_dataset():
    """Get dataset from environment or default"""
    return os.getenv('DATASET', 'gantry')

def extract_fulltext_content(session: Dict) -> Optional[str]:
    """Extract content from fulltext array"""
    if 'fulltext' not in session or not session['fulltext']:
        return None
    
    # Combine all fulltext entries
    texts = []
    for entry in session['fulltext']:
        if isinstance(entry, dict) and 'text' in entry:
            texts.append(entry['text'])
        elif isinstance(entry, str):
            texts.append(entry)
    
    return '\n\n'.join(texts) if texts else None

def extract_documents_content(session: Dict) -> Optional[str]:
    """Extract content from documents array"""
    if 'documents' not in session or not session['documents']:
        return None
    
    # Combine all document texts
    texts = []
    for doc in session['documents']:
        if isinstance(doc, dict) and 'text' in doc:
            texts.append(doc['text'])
    
    return '\n\n'.join(texts) if texts else None

def create_content_for_session(session: Dict, driver):
    """Create Content node for a session based on its type"""
    
    session_type = session.get('sessiontype', 'Unknown')
    session_guid = session.get('sessionguid')
    
    if not session_guid:
        return None
    
    # Extract content based on session type
    content = None
    source = None
    
    if session_type == 'Intel Report':
        content = extract_fulltext_content(session)
        source = 'intel_report'
    elif session_type == 'Social Network':
        content = extract_fulltext_content(session)
        source = 'social_media'
    elif session_type == 'Telephony':
        content = extract_documents_content(session)
        source = 'call_transcript'
    elif session_type == 'Generic File':
        content = extract_documents_content(session)
        source = 'document_file'
    elif session_type == 'Entity Report':
        content = extract_documents_content(session)
        source = 'entity_report'
    elif session_type == 'Collection Report':
        content = extract_fulltext_content(session)
        source = 'collection_report'
    
    if not content:
        return None
    
    # Create Content node
    with driver.session() as neo_session:
        query = """
        MATCH (s:Session {sessionguid: $session_guid})
        WHERE NOT EXISTS {
            MATCH (s)-[:HAS_CONTENT]->(c:Content {source: $source})
        }
        CREATE (c:Content {
            text: $text,
            session_id: $session_guid,
            source: $source,
            created_at: datetime(),
            sessionType: $session_type,
            contentType: $content_type,
            timestamp: $timestamp
        })
        CREATE (s)-[:HAS_CONTENT]->(c)
        RETURN c.source as created_source
        """
        
        result = neo_session.run(query, {
            "session_guid": session_guid,
            "text": content,
            "source": source,
            "session_type": session_type,
            "content_type": session.get('contenttype', 'Text'),
            "timestamp": session.get('sessiondate', datetime.now().isoformat())
        })
        
        record = result.single()
        return record["created_source"] if record else None

def process_ndjson_file(filename: str, driver):
    """Process sessions.ndjson and import additional content"""
    
    # Statistics
    stats = {
        'Intel Report': {'total': 0, 'imported': 0},
        'Social Network': {'total': 0, 'imported': 0},
        'Telephony': {'total': 0, 'imported': 0},
        'Generic File': {'total': 0, 'imported': 0},
        'Entity Report': {'total': 0, 'imported': 0},
        'Collection Report': {'total': 0, 'imported': 0}
    }
    
    print(f"Processing {filename}...")
    
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f):
            if line.strip():
                try:
                    session = json.loads(line)
                    session_type = session.get('sessiontype', 'Unknown')
                    
                    if session_type in stats:
                        stats[session_type]['total'] += 1
                        
                        # Process relevant session types
                        if session_type in ['Intel Report', 'Social Network', 'Telephony', 
                                          'Generic File', 'Entity Report', 'Collection Report']:
                            source = create_content_for_session(session, driver)
                            if source:
                                stats[session_type]['imported'] += 1
                                
                                if stats[session_type]['imported'] % 100 == 0:
                                    print(f"  {session_type}: {stats[session_type]['imported']} imported...")
                
                except json.JSONDecodeError as e:
                    print(f"Error parsing line {line_num + 1}: {e}")
                except Exception as e:
                    print(f"Error processing session at line {line_num + 1}: {e}")
    
    return stats

def main():
    """Main import function"""
    
    dataset = get_dataset()
    ndjson_file = f"data/{dataset}/sessions.ndjson"
    
    if not os.path.exists(ndjson_file):
        print(f"Error: {ndjson_file} not found")
        sys.exit(1)
    
    print(f"Importing additional content for dataset: {dataset}")
    print("=" * 60)
    
    # Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        # Get initial content stats
        with driver.session() as session:
            result = session.run("""
                MATCH (c:Content)
                RETURN c.source as source, count(c) as count
                ORDER BY count DESC
            """)
            
            print("Current Content nodes by source:")
            for record in result:
                print(f"  {record['source']}: {record['count']:,}")
            print()
        
        # Process the NDJSON file
        stats = process_ndjson_file(ndjson_file, driver)
        
        # Print results
        print("\nImport Results:")
        print("=" * 60)
        total_imported = 0
        for session_type, counts in stats.items():
            if counts['total'] > 0:
                pct = (counts['imported'] / counts['total']) * 100 if counts['total'] > 0 else 0
                print(f"{session_type}:")
                print(f"  Total sessions: {counts['total']:,}")
                print(f"  Imported content: {counts['imported']:,} ({pct:.1f}%)")
                total_imported += counts['imported']
        
        print(f"\nTotal new Content nodes: {total_imported:,}")
        
        # Final content stats
        print("\nFinal Content nodes by source:")
        with driver.session() as session:
            result = session.run("""
                MATCH (c:Content)
                RETURN c.source as source, count(c) as count
                ORDER BY count DESC
            """)
            
            for record in result:
                print(f"  {record['source']}: {record['count']:,}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        driver.close()

if __name__ == "__main__":
    main()