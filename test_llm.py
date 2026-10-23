from app.rag.llm import (
    generate_answer
)

response = generate_answer(
    "What is Retrieval Augmented Generation?"
)

print(response)