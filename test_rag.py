from app.rag.rag_pipeline import (
    RAGPipeline
)

rag = RAGPipeline()

answer = rag.ask(
    "What is Qdrant?"
)

print()
print(answer)