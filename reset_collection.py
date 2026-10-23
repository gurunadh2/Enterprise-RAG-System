from qdrant_client.models import (
    VectorParams,
    Distance
)

from app.database.qdrant_client import client

from app.core.config import (
    COLLECTION_NAME
)


client.delete_collection(
    COLLECTION_NAME
)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print(
    f"{COLLECTION_NAME} reset successfully"
)