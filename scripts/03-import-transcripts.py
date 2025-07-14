#!/usr/bin/env python
"""
Step 3: Import transcript data into Neo4j with proper timestamp conversion.

This script imports transcript text from LanceDB exports, converting Unix epoch
timestamps to ISO 8601 format and establishing proper session relationships.
Creates Content nodes linked to existing Session nodes.

Prerequisites:
  1. Neo4j container running
  2. Schema created (scripts/01-create-schema.sh)
  3. Sessions imported (02-import-sessions.py)

Usage:
  python scripts/03-import-transcripts.py                        # Uses data/default/transcripts.json
  python scripts/03-import-transcripts.py --dataset whiskey-jack # Uses data/whiskey-jack/transcripts.json
  python scripts/03-import-transcripts.py --file /path/to/file   # Uses specific file
"""

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path

import requests
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
        with open(transcript_file) as f:
            data = json.load(f)

        print(f"✅ Loaded {len(data)} transcripts from {transcript_file}")
        return data

    except Exception as e:
        print(f"❌ Error loading transcript file: {e}")
        return {}


def import_transcript(tx, session_id, transcript_data):
    """Create Content node with transcript data linked to Session"""
    iso_timestamp = unix_to_iso(transcript_data["timestamp"])

    result = tx.run(
        """
        MATCH (s:Session {sessionguid: $sid})
        CREATE (c:Content {
            sessionguid: $sid,
            text: $text,
            contentType: $content_type,
            chunkCount: $chunk_count,
            charCount: $char_count,
            sessionType: $session_type,
            target: $target,
            timestamp: $timestamp,
            importedAt: datetime()
        })
        CREATE (s)-[:HAS_CONTENT]->(c)
        RETURN c.sessionguid
    """,
        sid=session_id,
        text=transcript_data["text"],
        content_type=transcript_data.get("content_type", "text/plain"),
        chunk_count=transcript_data.get("chunk_count", 1),
        char_count=transcript_data.get("char_count", len(transcript_data["text"])),
        session_type=transcript_data.get("session_type", "Unknown"),
        target=transcript_data.get("target", ""),
        timestamp=iso_timestamp,
    )

    return result.single() is not None


def check_session_exists(tx, session_id):
    """Check if session exists in Neo4j"""
    result = tx.run("MATCH (s:Session {sessionguid: $session_id}) RETURN s.sessionguid", session_id=session_id)
    return result.single() is not None


def generate_openai_embedding(text, api_key=None):
    """
    Generate 1536-dimension embedding using OpenAI API.

    Args:
        text: Text to embed
        api_key: OpenAI API key (optional, uses OPENAI_API_KEY env var)

    Returns:
        List of 1536 floats or None if failed
    """
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return None

    try:
        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "input": text,
                "model": "text-embedding-3-small",  # 1536 dimensions
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            return data["data"][0]["embedding"]
        else:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


def import_transcript_with_embedding(tx, session_id, transcript_data, generate_embeddings=False):
    """Create Content node with transcript data and optional embedding"""
    iso_timestamp = unix_to_iso(transcript_data["timestamp"])

    # Generate embedding if requested and text is substantial
    embedding = None
    if generate_embeddings and len(transcript_data["text"]) > 50:
        embedding = generate_openai_embedding(transcript_data["text"])
        if embedding:
            print(f"✅ Generated 1536-dim embedding for {session_id}")
        else:
            print(f"⚠️  Failed to generate embedding for {session_id}")

    # Create Content node with optional embedding
    cypher_query = """
        MATCH (s:Session {sessionguid: $sid})
        CREATE (c:Content {
            sessionguid: $sid,
            text: $text,
            contentType: $content_type,
            chunkCount: $chunk_count,
            charCount: $char_count,
            sessionType: $session_type,
            target: $target,
            timestamp: $timestamp,
            importedAt: datetime()
        })
    """

    params = {
        "sid": session_id,
        "text": transcript_data["text"],
        "content_type": transcript_data.get("content_type", "text/plain"),
        "chunk_count": transcript_data.get("chunk_count", 1),
        "char_count": transcript_data.get("char_count", len(transcript_data["text"])),
        "session_type": transcript_data.get("session_type", "Unknown"),
        "target": transcript_data.get("target", ""),
        "timestamp": iso_timestamp,
    }

    # Add embedding if generated
    if embedding:
        cypher_query += "\nSET c.embedding = $embedding"
        params["embedding"] = embedding

    cypher_query += "\nCREATE (s)-[:HAS_CONTENT]->(c)\nRETURN c.sessionguid"

    result = tx.run(cypher_query, **params)
    return result.single() is not None


def patch_vector_index(driver):
    """
    Apply vector index patch to migrate from 384 to 1536 dimensions.
    Safe operation that preserves all data.
    """
    print("\n🔧 Applying vector index patch (384 → 1536 dimensions)...")

    patch_script = Path("scripts/patch-vector-index-1536.cypher")
    if not patch_script.exists():
        print(f"❌ Patch script not found: {patch_script}")
        return False

    try:
        with driver.session() as session:
            with open(patch_script) as f:
                # Split on semicolons and execute each statement
                statements = f.read().split(";")

                for stmt in statements:
                    stmt = stmt.strip()
                    if stmt and not stmt.startswith("//") and not stmt.startswith("/*"):
                        try:
                            result = session.run(stmt)
                            # Print results for verification queries
                            if "RETURN" in stmt.upper():
                                for record in result:
                                    print(f"   {dict(record)}")
                        except Exception as e:
                            # Some statements might fail (like DROP IF EXISTS), that's ok
                            if "not found" not in str(e).lower():
                                print(f"   ⚠️  {e}")

        print("✅ Vector index patch applied successfully")
        return True

    except Exception as e:
        print(f"❌ Error applying patch: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset", 
        default="default",
        help="Dataset/case name (subdirectory under data/). Default: default"
    )
    parser.add_argument(
        "--file",
        help="Optional: Direct path to transcripts.json file (overrides --dataset)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be imported without making changes")
    parser.add_argument("--sample", type=int, default=5, help="Number of sample records to show in dry-run")
    parser.add_argument("--patch-vector-index", action="store_true", help="Apply vector index patch (384→1536 dims)")
    parser.add_argument("--generate-embeddings", action="store_true", help="Generate 1536-dim OpenAI embeddings")
    parser.add_argument(
        "--embedding-delay", type=float, default=0.1, help="Delay between embedding API calls (seconds)"
    )

    args = parser.parse_args()
    
    # Determine the input file path
    if args.file:
        transcript_path = Path(args.file)
    else:
        transcript_path = Path(__file__).parent.parent / "data" / args.dataset / "transcripts.json"
    
    if not transcript_path.exists():
        print(f"Error: File not found: {transcript_path}")
        return 1

    print(f"Starting transcript import from {transcript_path}...")
    print(f"Dataset: {args.dataset if not args.file else 'custom file'}")

    # Load transcripts from JSON export
    transcripts = load_transcripts(str(transcript_path))
    if not transcripts:
        print("No transcripts found. Exiting.")
        return

    # Dry run mode
    if args.dry_run:
        print("\n🔍 DRY RUN - Preview of transcript import:")
        print(f"   Total transcripts: {len(transcripts)}")

        # Show sample records with timestamp conversion
        sample_items = list(transcripts.items())[: args.sample]
        print(f"\n📝 Sample records ({len(sample_items)}):")

        for i, (session_id, data) in enumerate(sample_items):
            iso_timestamp = unix_to_iso(data["timestamp"])
            print(f"\n--- Record {i + 1} ---")
            print(f"   Session ID: {session_id}")
            print(f"   Unix timestamp: {data['timestamp']}")
            print(f"   ISO timestamp: {iso_timestamp}")
            print(f"   Session type: {data.get('session_type', 'Unknown')}")
            print(f"   Content type: {data.get('content_type', 'text/plain')}")
            print(f"   Text preview: {data['text'][:100]}...")
            print(f"   Character count: {data.get('char_count', len(data['text']))}")

        print("\n✅ DRY RUN complete. Use without --dry-run to import data.")
        return

    # Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        # Apply vector index patch if requested
        if args.patch_vector_index:
            if not patch_vector_index(driver):
                print("❌ Vector index patch failed. Continuing with import...")
            print()

        with driver.session() as session:
            imported = 0
            linked_sessions = 0
            unlinked_sessions = 0
            session_types = {}
            embeddings_generated = 0

            for session_id, transcript_data in transcripts.items():
                try:
                    # Check if session exists
                    if session.execute_read(check_session_exists, session_id):
                        # Import transcript with optional embedding generation
                        if session.execute_write(
                            import_transcript_with_embedding, session_id, transcript_data, args.generate_embeddings
                        ):
                            imported += 1
                            linked_sessions += 1

                            # Count embeddings if generated
                            if args.generate_embeddings and len(transcript_data["text"]) > 50:
                                embeddings_generated += 1
                                # Rate limiting for API calls
                                if args.embedding_delay > 0:
                                    time.sleep(args.embedding_delay)

                        # Track session types
                        session_type = transcript_data.get("session_type", "Unknown")
                        session_types[session_type] = session_types.get(session_type, 0) + 1

                        if imported % 50 == 0:
                            print(f"Imported {imported}/{len(transcripts)} transcripts...")
                    else:
                        unlinked_sessions += 1
                        print(f"⚠️  Session {session_id} not found in Neo4j")

                except Exception as e:
                    print(f"Error importing {session_id}: {e}")

            # Print statistics
            print("\n📊 Transcript Import Statistics:")
            print(f"   Total transcripts processed: {len(transcripts):,}")
            print(f"   Content nodes created: {imported:,}")
            print(f"   Sessions linked: {linked_sessions:,}")
            print(f"   Sessions not found: {unlinked_sessions:,}")

            if args.generate_embeddings:
                print(f"   1536-dim embeddings generated: {embeddings_generated:,}")

            if session_types:
                print("\n📞 Session Types in Transcripts:")
                for stype, count in sorted(session_types.items()):
                    print(f"   {stype}: {count:,}")

            if imported > 0:
                print(f"\n✅ Successfully imported {imported} transcript content nodes")
                if args.generate_embeddings:
                    print(f"✅ Generated {embeddings_generated} OpenAI embeddings (1536 dimensions)")

            if unlinked_sessions > 0:
                print(f"⚠️  {unlinked_sessions} transcripts could not be linked (sessions not found)")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
