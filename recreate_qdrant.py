from app.database.qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

from app.core.config import (
    QDRANT_URL,
    COLLECTION_NAME
)

client = QdrantClient(
    url=QDRANT_URL
)

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384,
        distance="Cosine"
    )
)

print(
    f"{COLLECTION_NAME} collection created successfully!"
)