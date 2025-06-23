#!/usr/bin/env python3
"""
Import call transcripts into Neo4j Content nodes.
Reads JSON export from lancedb-call-transcripts-browser project.
"""
import os
import json
from neo4j import GraphDatabase

# Configuration
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "Sup3rSecur3!")

def load_transcripts():
    """
    Load transcript data from JSON export.
    Simple, no dependencies approach - "less is more".
    """
    transcript_file = "data/transcripts_export.json"
    
    if not os.path.exists(transcript_file):
        print(f"❌ Transcript file not found: {transcript_file}")
        print("Run export_for_neo4j.py in lancedb-call-transcripts-browser first")
        return {}
    
    try:
        with open(transcript_file, 'r') as f:
            data = json.load(f)
        
        # Extract just the text for each session
        transcripts = {session_id: info["text"] for session_id, info in data.items()}
        
        print(f"✅ Loaded {len(transcripts)} call transcripts from JSON export")
        return transcripts
        
    except Exception as e:
        print(f"❌ Error loading transcript file: {e}")
        return {}

def import_transcript(tx, session_id, text):
    """Create Content node with transcript text linked to Session"""
    tx.run("""
        MATCH (s:Session {sessionguid: $sid})
        CREATE (c:Content {
            id: randomUUID(),
            text: $txt,
            contentType: 'text/plain'
        })
        MERGE (s)-[:HAS_CONTENT]->(c)
    """, sid=session_id, txt=text)

def main():
    print("Starting transcript import from JSON export...")
    
    # Load transcripts from JSON export
    transcripts = load_transcripts()
    if not transcripts:
        print("No transcripts found. Exiting.")
        return
    
    # Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            imported = 0
            for session_id, text in transcripts.items():
                try:
                    session.execute_write(import_transcript, session_id, text)
                    imported += 1
                    if imported % 50 == 0:
                        print(f"Imported {imported}/{len(transcripts)} transcripts...")
                except Exception as e:
                    print(f"Error importing {session_id}: {e}")
            
            print(f"✓ Successfully imported {imported} call transcripts")
            
    finally:
        driver.close()

if __name__ == "__main__":
    main()