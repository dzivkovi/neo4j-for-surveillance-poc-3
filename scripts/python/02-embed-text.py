"""
compute embeddings for any Content node missing .embedding
"""

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Sup3rSecur3!"))
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

BATCH = 128
with driver.session() as sess:
    # pull batches lacking embedding
    result = sess.run("""
        MATCH (c:Content)
        WHERE c.text IS NOT NULL AND c.embedding IS NULL
        RETURN c.id AS cid, c.text AS text
    """)
    rows = list(result)

for i in tqdm(range(0, len(rows), BATCH), desc="Embedding"):
    batch = rows[i : i + BATCH]
    ids = [r["cid"] for r in batch]
    texts = [r["text"] for r in batch]
    vecs = model.encode(texts, normalize_embeddings=True)

    with driver.session() as sess:
        for cid, vec in zip(ids, vecs):
            sess.run(
                """
                MATCH (c:Content {id:$cid})
                SET c.embedding = $vec
            """,
                cid=cid,
                vec=vec.tolist(),
            )
print("✔ embeddings stored")
