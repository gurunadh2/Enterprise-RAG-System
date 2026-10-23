from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny
)

from app.database.qdrant_client import client
from app.rag.embedder import get_embedding

from app.core.config import (
    COLLECTION_NAME,
    TOP_K
)


def vector_search(
    query,
    username,
    limit=TOP_K,
    source_filter=None
):

    query_vector = get_embedding(
        query
    )

    conditions = [
        FieldCondition(
            key="username",
            match=MatchValue(
                value=username
            )
        )
    ]

    if source_filter:

        conditions.append(
            FieldCondition(
                key="source",
                match=MatchAny(
                    any=source_filter
                )
            )
        )

    search_filter = Filter(
        must=conditions
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        query_filter=search_filter
    )

    formatted_results = []

    for point in results.points:

        formatted_results.append(
            {
                "text": point.payload["text"],
                "source": point.payload["source"],
                "chunk_id": point.payload["chunk_id"],
                "score": point.score
            }
        )

    return formatted_results