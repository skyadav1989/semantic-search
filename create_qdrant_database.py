from qdrant_client.http.exceptions import ResponseHandlingException

from app.config import get_settings
from app.embedding.bge_m3_embedder import BGEM3Embedder
from app.embedding.qdrant_manager import QdrantCollectionManager


def main() -> int:
    settings = get_settings()
    collection = settings.QDRANT_COLLECTION

    manager = QdrantCollectionManager(
        url=settings.qdrant_url,
        api_key=settings.QDRANT_API_KEY,
        timeout=5,
    )
    client = manager.client

    try:
        if client.collection_exists(collection):
            client.delete_collection(collection)
    except ResponseHandlingException as exc:
        print(f"Unable to connect to Qdrant at {settings.qdrant_url}.")
        print("Start Qdrant and try again, or update QDRANT_URL/QDRANT_HOST/QDRANT_PORT in .env.")
        print(f"Details: {exc}")
        return 1

    embedder = BGEM3Embedder(
        model_name=settings.EMBEDDING_MODEL,
        device=settings.EMBEDDING_DEVICE,
    )

    dimension = embedder.dimension

    manager.create(
        collection=collection,
        dimension=dimension,
    )
    print(f"Collection created: {collection}")

    info = client.get_collection(collection)

    print(info)
    print(client.count(collection, exact=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
