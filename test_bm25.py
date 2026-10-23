from app.rag.bm25_retriever import BM25Retriever

documents = [
    "Qdrant is a vector database",
    "FastAPI builds APIs",
    "LangChain builds RAG systems",
    "Hybrid search combines BM25 and vectors"
]

retriever = BM25Retriever(documents)

results = retriever.search(
    "What is BM25?"
)

for doc, score in results:
    print(score, doc)