"""
Query Neo4j vector index (via LangChain retriever) to answer:

  "Does Fred discuss travel plans?"
"""
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

# Initialize the embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Sup3rSecur3!"))

def semantic_search(query_text, top_k=5):
    """Perform semantic search using vector similarity"""
    # Generate embedding for the query
    query_embedding = model.encode(query_text).tolist()

    with driver.session() as session:
        result = session.run("""
            CALL db.index.vector.queryNodes('ContentVectorIndex', $k, $query_vector)
            YIELD node, score
            MATCH (s:Session)-[:HAS_CONTENT]->(node)
            RETURN node.id as content_id,
                   node.text as content_text,
                   s.sessionguid as session_id,
                   s.sessiontype as session_type,
                   score
            ORDER BY score DESC
        """, k=top_k, query_vector=query_embedding)

        return list(result)

# Search for travel-related content
print("Searching for: 'travel plans vacation trip'")
results = semantic_search("travel plans vacation trip", top_k=5)

print(f"\nTop {len(results)} similarity hits:")
for i, record in enumerate(results, 1):
    content_preview = record["content_text"][:120].replace("\n", " ") if record["content_text"] else "No text"
    print(f"{i}. Score: {record['score']:.4f}")
    print(f"   Session: {record['session_id']} ({record['session_type']})")
    print(f"   Content: {content_preview}...")
    print()

# Search for specific person mentions
print("\nSearching for: 'Fred Merlin contact information'")
fred_results = semantic_search("Fred Merlin contact information", top_k=3)

print(f"\nFred-related results ({len(fred_results)} hits):")
for i, record in enumerate(fred_results, 1):
    content_preview = record["content_text"][:150].replace("\n", " ") if record["content_text"] else "No text"
    print(f"{i}. Score: {record['score']:.4f}")
    print(f"   Content: {content_preview}...")
    print()

# Close the driver
driver.close()

print("Demo complete! You can modify the search terms to explore different concepts.")
