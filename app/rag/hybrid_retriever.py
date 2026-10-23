from app.rag.bm25_retriever import BM25Retriever
from app.rag.document_store import get_all_documents
from app.rag.retriever import vector_search
from app.rag.fusion import reciprocal_rank_fusion


class HybridRetriever:

    def __init__(self):

        docs = get_all_documents()

        if len(docs) == 0:

            self.bm25 = None

        else:

            self.bm25 = BM25Retriever(
                docs
            )

    def search(
        self,
        query,
        username,
        source_filter=None
    ):

        vector_results = vector_search(
            query,
            username,
            limit=5,
            source_filter=source_filter
        )

        if self.bm25 is None:

            return vector_results

        bm25_results = self.bm25.search(
            query,
            top_k=5,
            source_filter=source_filter,
            username=username
        )

        return reciprocal_rank_fusion(
            bm25_results,
            vector_results
        )