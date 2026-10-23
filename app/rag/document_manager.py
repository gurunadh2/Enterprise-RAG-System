from collections import defaultdict

from app.database.qdrant_client import client
from app.core.config import COLLECTION_NAME


def get_document_summary(
    username=None
):

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True,
        with_vectors=False
    )

    docs = defaultdict(int)

    for point in points:

        if username:

            if point.payload.get(
                "username"
            ) != username:

                continue

        source = point.payload["source"]

        docs[source] += 1

    result = []

    for filename, chunks in docs.items():

        result.append(
            {
                "filename": filename,
                "chunks": chunks
            }
        )

    return result


def delete_document(
    filename,
    username=None
):

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True,
        with_vectors=False
    )

    ids_to_delete = []

    for point in points:

        if username:

            if point.payload.get(
                "username"
            ) != username:

                continue

        if point.payload["source"] == filename:

            ids_to_delete.append(
                point.id
            )

    if ids_to_delete:

        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=ids_to_delete
        )

    return len(ids_to_delete)