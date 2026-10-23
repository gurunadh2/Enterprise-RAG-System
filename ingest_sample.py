from app.rag.document_processor import (
    process_document
)

from app.rag.ingestion import (
    store_chunks
)

with open(
    "app/data/documents/sample.txt",
    "r",
    encoding="utf-8"
) as file:

    text = file.read()

chunks = process_document(
    text,
    "sample.txt"
)

store_chunks(chunks)