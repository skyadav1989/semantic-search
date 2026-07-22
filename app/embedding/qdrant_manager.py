try:
    from qdrant_client import QdrantClient
    from qdrant_client.http.models import Distance, VectorParams
except ImportError:
    QdrantClient = None
    Distance = None
    VectorParams = None


class QdrantCollectionManager:
    """
    Create and manage Qdrant collections.
    """

    def __init__(
        self,
        url="http://localhost:6333",
        api_key=None,
    ):
        if QdrantClient is None:
            raise ImportError(
                "Please install qdrant-client"
            )

        self.client = QdrantClient(
            url=url,
            api_key=api_key,
        )

    def exists(self, collection):
        return self.client.collection_exists(collection)

    def create(
        self,
        collection,
        dimension=1024,
        distance=None,
    ):

        if distance is None:
            distance = Distance.COSINE

        if self.exists(collection):
            return False

        self.client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=dimension,
                distance=distance,
            ),
        )

        return True

    def info(self, collection):
        return self.client.get_collection(collection)