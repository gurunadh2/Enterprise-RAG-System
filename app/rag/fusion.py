def reciprocal_rank_fusion(
    bm25_results,
    vector_results,
    k=60
):

    scores = {}

    metadata = {}

    for rank, result in enumerate(
        bm25_results,
        start=1
    ):

        doc = result["text"]

        metadata[doc] = {
            "source": result["source"],
            "chunk_id": result["chunk_id"]
        }

        scores[doc] = scores.get(
            doc,
            0
        ) + 1 / (k + rank)

    for rank, result in enumerate(
        vector_results,
        start=1
    ):

        doc = result["text"]

        metadata[doc] = {
            "source": result["source"],
            "chunk_id": result["chunk_id"]
        }

        scores[doc] = scores.get(
            doc,
            0
        ) + 1 / (k + rank)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    final_results = []

    for doc, score in ranked:

        final_results.append(
            {
                "text": doc,
                "score": score,
                "source": metadata[doc]["source"],
                "chunk_id": metadata[doc]["chunk_id"]
            }
        )

    return final_results