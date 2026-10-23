from app.rag.embedder import get_embedding

embedding = get_embedding(
    "What is Retrieval Augmented Generation?"
)

print(len(embedding))