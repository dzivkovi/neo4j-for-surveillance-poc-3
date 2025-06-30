#!/usr/bin/env python
"""
Import LanceDB transcript data into Neo4j with proper timestamp conversion.

This script imports transcript text from LanceDB exports, converting Unix epoch 
timestamps to ISO 8601 format and establishing proper session relationships.
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path
import argparse
from neo4j import GraphDatabase

# Configuration
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "Sup3rSecur3!")

def unix_to_iso(unix_timestamp):
    """Convert Unix epoch timestamp to ISO 8601 format."""
    return datetime.fromtimestamp(unix_timestamp).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def load_transcripts(transcript_file):
    """
    Load transcript data from LanceDB JSON export.
    Handles the current format with Unix timestamps.
    """
    if not os.path.exists(transcript_file):
        print(f"❌ Transcript file not found: {transcript_file}")
        return {}
    
    try:
        with open(transcript_file, 'r') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} transcripts from {transcript_file}")
        return data
        
    except Exception as e:
        print(f"❌ Error loading transcript file: {e}")
        return {}

def import_transcript(tx, session_id, transcript_data):
    """Create Content node with transcript data linked to Session"""
    iso_timestamp = unix_to_iso(transcript_data['timestamp'])
    
    result = tx.run("""
        MATCH (s:Session {sessionguid: $sid})
        CREATE (c:Content {
            sessionguid: $sid,
            text: $text,
            contentType: $contentType,
            chunkCount: $chunkCount,
            charCount: $charCount,
            sessionType: $sessionType,
            target: $target,
            timestamp: $timestamp,
            importedAt: datetime()
        })
        CREATE (s)-[:HAS_CONTENT]->(c)
        RETURN c.sessionguid
    """, 
        sid=session_id,
        text=transcript_data['text'],
        contentType=transcript_data.get('content_type', 'text/plain'),
        chunkCount=transcript_data.get('chunk_count', 1),
        charCount=transcript_data.get('char_count', len(transcript_data['text'])),
        sessionType=transcript_data.get('session_type', 'Unknown'),
        target=transcript_data.get('target', ''),
        timestamp=iso_timestamp
    )
    
    return result.single() is not None

def check_session_exists(tx, session_id):
    """Check if session exists in Neo4j"""
    result = tx.run(
        "MATCH (s:Session {sessionguid: $sessionId}) RETURN s.sessionguid",
        sessionId=session_id
    )
    return result.single() is not None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transcript_file', nargs='?', default='data/transcripts.json', help='JSON file with transcript data')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be imported without making changes')
    parser.add_argument('--sample', type=int, default=5, help='Number of sample records to show in dry-run')
    
    args = parser.parse_args()
    
    print(f"Starting transcript import from {args.transcript_file}...")
    
    # Load transcripts from JSON export
    transcripts = load_transcripts(args.transcript_file)
    if not transcripts:
        print("No transcripts found. Exiting.")
        return
    
    # Dry run mode
    if args.dry_run:
        print(f"\n🔍 DRY RUN - Preview of transcript import:")
        print(f"   Total transcripts: {len(transcripts)}")
        
        # Show sample records with timestamp conversion
        sample_items = list(transcripts.items())[:args.sample]
        print(f"\n📝 Sample records ({len(sample_items)}):")
        
        for i, (session_id, data) in enumerate(sample_items):
            iso_timestamp = unix_to_iso(data['timestamp'])
            print(f"\n--- Record {i+1} ---")
            print(f"   Session ID: {session_id}")
            print(f"   Unix timestamp: {data['timestamp']}")
            print(f"   ISO timestamp: {iso_timestamp}")
            print(f"   Session type: {data.get('session_type', 'Unknown')}")
            print(f"   Content type: {data.get('content_type', 'text/plain')}")
            print(f"   Text preview: {data['text'][:100]}...")
            print(f"   Character count: {data.get('char_count', len(data['text']))}")
        
        print(f"\n✅ DRY RUN complete. Use without --dry-run to import data.")
        return
    
    # Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            imported = 0
            linked_sessions = 0
            unlinked_sessions = 0
            session_types = {}
            
            for session_id, transcript_data in transcripts.items():
                try:
                    # Check if session exists
                    if session.execute_read(check_session_exists, session_id):
                        # Import transcript
                        if session.execute_write(import_transcript, session_id, transcript_data):
                            imported += 1
                            linked_sessions += 1
                        
                        # Track session types
                        session_type = transcript_data.get('session_type', 'Unknown')
                        session_types[session_type] = session_types.get(session_type, 0) + 1
                        
                        if imported % 50 == 0:
                            print(f"Imported {imported}/{len(transcripts)} transcripts...")
                    else:
                        unlinked_sessions += 1
                        print(f"⚠️  Session {session_id} not found in Neo4j")
                        
                except Exception as e:
                    print(f"Error importing {session_id}: {e}")
            
            # Print statistics
            print(f"\n📊 Transcript Import Statistics:")
            print(f"   Total transcripts processed: {len(transcripts):,}")
            print(f"   Content nodes created: {imported:,}")
            print(f"   Sessions linked: {linked_sessions:,}")
            print(f"   Sessions not found: {unlinked_sessions:,}")
            
            if session_types:
                print(f"\n📞 Session Types in Transcripts:")
                for stype, count in sorted(session_types.items()):
                    print(f"   {stype}: {count:,}")
            
            if imported > 0:
                print(f"\n✅ Successfully imported {imported} transcript content nodes")
            
            if unlinked_sessions > 0:
                print(f"⚠️  {unlinked_sessions} transcripts could not be linked (sessions not found)")
            
    finally:
        driver.close()

if __name__ == "__main__":
    main()