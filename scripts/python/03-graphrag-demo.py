#!/usr/bin/env python
"""
Query Neo4j vector index (via LangChain retriever) to answer:

  "Does Fred discuss travel plans?"
"""

import os
import asyncio
from langchain_community.vectorstores import Neo4jVector
from langchain.schema import Document


NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Sup3rSecur3!")


async def graphrag_demo():
    """Demonstrate GraphRAG capabilities with Neo4j and LangChain."""
    # Initialize embeddings - use OpenAI for 1536 dimensions to match database
    from langchain_community.embeddings import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # 1536 dimensions

    # Create Neo4j vector store instance
    vector_store = Neo4jVector.from_existing_index(
        embedding=embeddings,
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        index_name="ContentVectorIndex",  # Use correct PascalCase index name for Neo4j
        node_label="Content",
        text_node_property="text",
        embedding_node_property="embedding",
    )

    # Query about Fred's travel plans
    question = "Does Fred discuss travel plans?"
    print(f"🔍 Question: {question}\n")

    # Perform similarity search
    results = vector_store.similarity_search(question, k=5)

    if results:
        print(f"✅ Found {len(results)} relevant content pieces:\n")
        for i, doc in enumerate(results, 1):
            print(f"{i}. Content excerpt:")
            print(f"   {doc.page_content[:200]}...")
            if hasattr(doc, "metadata"):
                print(f"   Metadata: {doc.metadata}")
            print()
    else:
        print("❌ No relevant content found.\n")

    # Enhanced query with context
    print("\n🔍 Enhanced Query: Finding specific travel mentions...")
    travel_query = "travel Miami meeting February"
    travel_results = vector_store.similarity_search(travel_query, k=3)

    if travel_results:
        print(f"\n✅ Found {len(travel_results)} travel-related discussions:\n")
        for i, doc in enumerate(travel_results, 1):
            print(f"{i}. {doc.page_content[:300]}...")
            print()


def main():
    """Run the GraphRAG demo."""
    print("=== Neo4j GraphRAG Demo ===\n")
    print("This demo uses LangChain's Neo4jVector to query our graph database")
    print("using natural language via vector similarity search.\n")

    asyncio.run(graphrag_demo())

    print("\n=== Analysis Complete ===")
    print("\nThis demonstrates how GraphRAG can answer investigative questions")
    print("by combining graph traversal with semantic search capabilities.")


if __name__ == "__main__":
    main()
