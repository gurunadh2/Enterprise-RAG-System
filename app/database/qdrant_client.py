from qdrant_client import QdrantClient

from app.core.config import (
    QDRANT_URL
)

client = QdrantClient(
    url=QDRANT_URL
)