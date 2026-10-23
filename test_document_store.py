from app.rag.document_store import (
    get_all_documents
)

docs = get_all_documents()

print()

print("Documents Found:", len(docs))

for doc in docs:

    print()
    print(doc)