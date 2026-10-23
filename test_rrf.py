from app.rag.hybrid_retriever import (
    HybridRetriever
)

retriever = HybridRetriever()

results = retriever.search(
    "What is vector database?"
)

print()

for doc, score in results:

    print()
    print("Score:", score)
    print(doc)