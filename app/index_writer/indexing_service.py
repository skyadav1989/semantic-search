from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


class IndexingService:

    def __init__(
        self,
        client: QdrantClient,
        collection: str = "products",
    ):
        self.client = client
        self.collection = collection

    def index(
        self,
        product_id,
        vector,
        payload,
    ):

        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=str(product_id),
                    vector=vector,
                    payload=payload,
                )
            ],
        )