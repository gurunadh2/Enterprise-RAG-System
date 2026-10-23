from app.rag.hybrid_retriever import (
    HybridRetriever
)

from app.chat.database import (
    save_chat
)

from app.rag.prompt_builder import (
    build_prompt
)

from app.rag.llm import (
    generate_answer
)

from app.evaluation.hallucination import (
    evaluate_answer
)


class RAGPipeline:

    def __init__(self):

        self.retriever = (
            HybridRetriever()
        )

    def ask(
        self,
        question,
        username,
        source_filter=None
    ):

        results = self.retriever.search(
            question,
            username,
            source_filter=source_filter
        )

        context = "\n\n".join(
            [
                item["text"]
                for item in results[:3]
            ]
        )

        prompt = build_prompt(
            question,
            context
        )

        print("\n===== PROMPT DEBUG =====")
        print(prompt[:2000])
        print("===== END PROMPT =====\n")


        answer = generate_answer(
            prompt
        )

        save_chat(
           username,
           question,
           answer
        )

        evaluation = evaluate_answer(
            question,
            answer,
            context
        )

        citations = []

        for item in results[:3]:

            citations.append(
                {
                    "file": item["source"],
                    "chunk_id": item["chunk_id"],
                    "text": item["text"]
                }
            )

        return {
            "answer": answer,
            "sources": citations,
            "evaluation": evaluation
        }