from app.rag.document_processor import (
    process_document
)

from app.rag.ingestion import (
    store_chunks
)


def index_document(
    text,
    filename,
    username
):

    if not text.strip():

        raise ValueError(
            "No text extracted from document."
        )

    chunks = process_document(
        text,
        filename
    )

    if not chunks:

        raise ValueError(
            "No chunks created."
        )

    store_chunks(
        chunks,
        username
    )

    print(
        f"Indexed {len(chunks)} chunks from {filename} for {username}"
    )

    return len(chunks)