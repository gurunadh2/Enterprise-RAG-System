from app.database.qdrant_client import client
from app.core.config import COLLECTION_NAME

client.delete_collection(
    collection_name=COLLECTION_NAME
)

print("Collection deleted successfully")