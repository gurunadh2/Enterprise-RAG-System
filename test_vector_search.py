from app.rag.retriever import (
    vector_search
)

results = vector_search(
    "What is vector database?"
)

for result in results:

    print()
    print(result.score)

    print(
        result.payload["text"]
    )