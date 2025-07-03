#!/usr/bin/env python
"""
OpenAI Embeddings for Content Nodes
===================================

Generates 1536-dimensional embeddings using OpenAI's text-embedding-3-small model
for any Content node missing .embedding_v2

This replaces the local sentence-transformers approach with production-ready
OpenAI embeddings for improved semantic search accuracy.
"""

import os
import sys
import time
from typing import Any

import openai
from neo4j import GraphDatabase
from tqdm import tqdm


def load_config():
    """Load configuration from environment variables"""
    config = {
        "neo4j_uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "neo4j_username": os.getenv("NEO4J_USERNAME", "neo4j"),
        "neo4j_password": os.getenv("NEO4J_PASSWORD", "Sup3rSecur3!"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "embedding_model": os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        "batch_size": int(os.getenv("EMBEDDING_BATCH_SIZE", "1")),
        "rate_limit_delay": float(os.getenv("RATE_LIMIT_DELAY", "0.1")),
    }

    if not config["openai_api_key"]:
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key in the .env file")
        sys.exit(1)

    return config


def get_content_without_embeddings(driver) -> list[dict[str, Any]]:
    """Get Content nodes that don't have OpenAI embeddings yet"""
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Content)
            WHERE c.text IS NOT NULL AND c.embedding IS NULL
            RETURN elementId(c) AS node_id, c.text AS text, c.sessionguid AS sessionguid, c.timestamp AS timestamp
        """)
        return list(result)


def truncate_text(text: str, max_tokens: int = 8000) -> str:
    """Truncate text to fit within token limits (rough estimate: 4 chars = 1 token)"""
    max_chars = max_tokens * 4
    if len(text) > max_chars:
        return text[:max_chars]
    return text


def generate_embeddings_batch(client: openai.OpenAI, texts: list[str], model: str) -> list[list[float]]:
    """Generate embeddings for a batch of texts using OpenAI API"""
    try:
        # Truncate texts to prevent token limit issues
        truncated_texts = [truncate_text(text) for text in texts]

        response = client.embeddings.create(model=model, input=truncated_texts)
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"ERROR generating embeddings: {e}")
        raise


def store_embeddings_batch(driver, content_ids: list[str], embeddings: list[list[float]]):
    """Store embeddings back to Neo4j Content nodes"""
    with driver.session() as session:
        for node_id, embedding in zip(content_ids, embeddings):
            session.run(
                """
                MATCH (c:Content)
                WHERE elementId(c) = $node_id
                SET c.embedding = $embedding
            """,
                node_id=node_id,
                embedding=embedding,
            )


def main():
    """Main embedding generation process"""
    print("🚀 Starting OpenAI embedding generation for Content nodes...")

    # Load configuration
    config = load_config()
    print(f"📊 Configuration: Model={config['embedding_model']}, Batch size={config['batch_size']}")

    # Initialize connections
    driver = GraphDatabase.driver(config["neo4j_uri"], auth=(config["neo4j_username"], config["neo4j_password"]))

    client = openai.OpenAI(api_key=config["openai_api_key"])

    try:
        # Get content that needs embeddings
        print("📋 Finding Content nodes without OpenAI embeddings...")
        rows = get_content_without_embeddings(driver)

        if not rows:
            print("✅ All Content nodes already have OpenAI embeddings!")
            return

        print(f"🎯 Found {len(rows)} Content nodes needing embeddings")

        # Process in batches
        batch_size = config["batch_size"]
        total_cost_estimate = len(rows) * 0.00013 / 1000  # Rough cost estimate
        print(f"💰 Estimated cost: ~${total_cost_estimate:.4f}")

        for i in tqdm(range(0, len(rows), batch_size), desc="Generating embeddings"):
            batch = rows[i : i + batch_size]
            node_ids = [r["node_id"] for r in batch]
            texts = [r["text"] for r in batch]

            # Generate embeddings
            embeddings = generate_embeddings_batch(client, texts, config["embedding_model"])

            # Verify embedding dimensions
            for j, embedding in enumerate(embeddings):
                if len(embedding) != 1536:
                    print(f"⚠️  Warning: Embedding {j} has {len(embedding)} dimensions, expected 1536")

            # Store to Neo4j
            store_embeddings_batch(driver, node_ids, embeddings)

            # Rate limiting
            if config["rate_limit_delay"] > 0:
                time.sleep(config["rate_limit_delay"])

        print("✅ OpenAI embeddings generation completed successfully!")

        # Verify results
        with driver.session() as session:
            result = session.run("""
                MATCH (c:Content)
                RETURN
                    count(CASE WHEN c.embedding IS NOT NULL THEN 1 END) as with_openai_embeddings,
                    count(*) as total_content,
                    avg(size(c.embedding)) as avg_dimensions
            """)
            stats = result.single()
            print(
                f"📈 Final stats: {stats['with_openai_embeddings']}/{stats['total_content']} nodes have OpenAI embeddings"
            )
            print(f"📏 Average embedding dimensions: {stats['avg_dimensions']}")

    except Exception as e:
        print(f"❌ Error during embedding generation: {e}")
        raise

    finally:
        driver.close()


if __name__ == "__main__":
    main()
