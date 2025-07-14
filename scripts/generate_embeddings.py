#!/usr/bin/env python3
"""
Complete embedding generation for all Content nodes with optimized batching.
This script handles the full dataset with proper error handling and progress tracking.
"""

import os
import sys
import time
import math
from neo4j import GraphDatabase
from tqdm import tqdm

def get_neo4j_connection():
    """Get Neo4j connection based on dataset environment variable."""
    dataset = os.getenv('DATASET', 'default')
    uri = f"bolt://localhost:7687"
    return GraphDatabase.driver(uri, auth=("neo4j", "Sup3rSecur3!"))

def get_content_stats(driver):
    """Get comprehensive content statistics."""
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Content)
            RETURN 
                count(c) as total_content,
                count(c.text) as with_text,
                count(c.embedding) as with_embeddings,
                count(c.text) - count(c.embedding) as needs_embedding
        """)
        return result.single()

def get_optimal_batch_size(driver, api_key):
    """Test optimal batch size based on content length."""
    with driver.session() as session:
        # Get sample content lengths
        result = session.run("""
            MATCH (c:Content)
            WHERE c.text IS NOT NULL AND c.embedding IS NULL
            RETURN avg(size(c.text)) as avg_length,
                   max(size(c.text)) as max_length,
                   min(size(c.text)) as min_length
            LIMIT 1000
        """)
        stats = result.single()
        
        if not stats or stats['avg_length'] is None:
            return 10
        
        avg_length = stats['avg_length']
        # Truncate to 1500 chars max, estimate tokens as chars/4
        estimated_tokens_per_doc = min(1500, avg_length) / 4
        
        # Target 200K tokens per batch (leave 100K buffer)
        optimal_batch = max(10, min(200, int(200000 / estimated_tokens_per_doc)))
        
        print(f"Content stats: avg={avg_length:.0f}, max={stats['max_length']}, min={stats['min_length']}")
        print(f"Optimal batch size: {optimal_batch}")
        
        return optimal_batch

def generate_embeddings_optimized(driver, api_key, batch_size=50):
    """Generate embeddings with optimized batching and error handling."""
    
    total_processed = 0
    failed_batches = 0
    
    # Get total work to do
    stats = get_content_stats(driver)
    total_needed = stats['needs_embedding']
    
    print(f"Processing {total_needed} nodes needing embeddings...")
    
    # Create progress bar
    pbar = tqdm(total=total_needed, desc="Embedding progress")
    
    while True:
        try:
            with driver.session() as session:
                result = session.run("""
                    MATCH (c:Content)
                    WHERE c.text IS NOT NULL AND c.embedding IS NULL
                    WITH c
                    ORDER BY c.sessionguid
                    LIMIT $batch_size
                    WITH collect(c) AS nodes
                    WITH nodes, [n IN nodes | substring(n.text, 0, 1500)] AS texts
                    WHERE size(texts) > 0
                    CALL genai.vector.encodeBatch(texts, 'OpenAI', {
                        token: $api_key,
                        model: 'text-embedding-3-small',
                        dimensions: 1536
                    }) YIELD index, vector
                    WITH nodes[index] AS node, vector
                    CALL db.create.setNodeVectorProperty(node, 'embedding', vector)
                    RETURN count(node) as nodes_embedded
                """, {"batch_size": batch_size, "api_key": api_key})
                
                record = result.single()
                nodes_embedded = record["nodes_embedded"]
                
                if nodes_embedded == 0:
                    break
                
                total_processed += nodes_embedded
                pbar.update(nodes_embedded)
                
                # Rate limiting
                time.sleep(0.1)
                
        except Exception as e:
            failed_batches += 1
            print(f"\nBatch failed: {e}")
            
            if failed_batches > 5:
                print("Too many failures, stopping...")
                break
                
            # Reduce batch size on failure
            batch_size = max(5, batch_size // 2)
            print(f"Reducing batch size to {batch_size}")
            time.sleep(1)
            continue
    
    pbar.close()
    return total_processed, failed_batches

def main():
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    print(f"Using OpenAI API key: {api_key[:7]}...")
    
    # Connect to Neo4j
    driver = get_neo4j_connection()
    
    try:
        # Get initial stats
        print("Initial status:")
        stats = get_content_stats(driver)
        print(f"  Total Content: {stats['total_content']:,}")
        print(f"  With text: {stats['with_text']:,}")
        print(f"  With embeddings: {stats['with_embeddings']:,}")
        print(f"  Needs embedding: {stats['needs_embedding']:,}")
        
        if stats['needs_embedding'] == 0:
            print("All nodes already have embeddings!")
            return
        
        # Get optimal batch size
        batch_size = get_optimal_batch_size(driver, api_key)
        
        # Generate embeddings
        print(f"\nGenerating embeddings with batch size {batch_size}...")
        total_processed, failed_batches = generate_embeddings_optimized(driver, api_key, batch_size)
        
        # Final stats
        print(f"\nFinal status:")
        final_stats = get_content_stats(driver)
        print(f"  Total Content: {final_stats['total_content']:,}")
        print(f"  With text: {final_stats['with_text']:,}")
        print(f"  With embeddings: {final_stats['with_embeddings']:,}")
        print(f"  Still needs embedding: {final_stats['needs_embedding']:,}")
        
        # Calculate completion percentage
        completion = (final_stats['with_embeddings'] / final_stats['with_text']) * 100
        print(f"\nCompletion: {completion:.1f}%")
        print(f"Processed: {total_processed:,} nodes")
        print(f"Failed batches: {failed_batches}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        driver.close()

if __name__ == "__main__":
    main()