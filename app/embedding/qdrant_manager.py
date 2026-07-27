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
        url=None,
        api_key=None,
        timeout=5,
    ):
        if QdrantClient is None:
            raise ImportError(
                "Please install qdrant-client"
            )

        if url is None or api_key is None:
            from app.config import get_settings

            settings = get_settings()
            url = url or settings.qdrant_url
            api_key = api_key if api_key is not None else settings.QDRANT_API_KEY

        self.client = QdrantClient(
            url=url,
            api_key=api_key,
            timeout=timeout,
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
