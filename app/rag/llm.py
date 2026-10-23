from ollama import Client

from app.core.config import (
    OLLAMA_MODEL
)

client = Client(
    host="http://localhost:11434"
)


def generate_answer(prompt):

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]