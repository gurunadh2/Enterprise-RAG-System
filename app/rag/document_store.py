from app.database.qdrant_client import client

from app.core.config import (
    COLLECTION_NAME
)


def get_all_documents():

    documents = []

    try:

        collections = client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if COLLECTION_NAME not in collection_names:

            return documents

        offset = None

        while True:

            points, offset = client.scroll(
                collection_name=COLLECTION_NAME,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )

            for point in points:

                documents.append(
                    {
                        "text": point.payload["text"],
                        "source": point.payload["source"],
                        "chunk_id": point.payload["chunk_id"],
                        "username": point.payload.get(
                            "username",
                            ""
                        )
                    }
                )

            if offset is None:

                break

    except Exception as e:

        print(
            f"Document store error: {e}"
        )

    return documents
