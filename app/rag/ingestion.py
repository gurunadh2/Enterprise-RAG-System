from uuid import uuid4

from qdrant_client.models import (
    PointStruct
)

from app.database.qdrant_client import client
from app.rag.embedder import get_embedding

from app.core.config import (
    COLLECTION_NAME
)


def store_chunks(
    chunks,
    username
):

    points = []

    for chunk in chunks:

        embedding = get_embedding(
            chunk["text"]
        )

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "username": username
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(
        f"Stored {len(points)} chunks for {username}"
    )