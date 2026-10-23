from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, documents):

        self.documents = documents

        tokenized_docs = [
            doc["text"].lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_docs
        )

    def search(
        self,
        query,
        top_k=5,
        source_filter=None,
        username=None
    ):

        tokenized_query = (
            query.lower().split()
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked = sorted(
            zip(
                self.documents,
                scores
            ),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for doc, score in ranked:

            # User filter
            if username:

                if doc.get(
                    "username"
                ) != username:

                    continue

            # Document filter
            if source_filter:

                if doc["source"] not in source_filter:

                    continue

            results.append(
                {
                    "text": doc["text"],
                    "source": doc["source"],
                    "chunk_id": doc["chunk_id"],
                    "score": float(score)
                }
            )

            if len(results) >= top_k:

                break

        return results