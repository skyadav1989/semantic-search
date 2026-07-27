from dataclasses import dataclass

from app.config import get_settings


@dataclass
class Settings:

    embedding_model: str | None = None

    device: str | None = None

    collection_name: str | None = None

    qdrant_host: str | None = None

    qdrant_port: int | None = None

    top_k: int = 20

    def __post_init__(self):
        settings = get_settings()

        self.embedding_model = self.embedding_model or settings.EMBEDDING_MODEL
        self.device = self.device or settings.EMBEDDING_DEVICE
        self.collection_name = self.collection_name or settings.QDRANT_COLLECTION
        self.qdrant_host = self.qdrant_host or settings.QDRANT_HOST
        self.qdrant_port = self.qdrant_port or settings.QDRANT_PORT
