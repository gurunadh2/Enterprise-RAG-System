from app.rag.chunker import recursive_chunking

def process_document(text, filename):

    chunks = recursive_chunking(text)

    processed_chunks = []

    for idx, chunk in enumerate(chunks):

        processed_chunks.append(
            {
                "chunk_id": idx,
                "text": chunk,
                "source": filename
            }
        )

    return processed_chunks