import os

from dotenv import load_dotenv

load_dotenv()


QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "documents"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3"
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        "5"
    )
)