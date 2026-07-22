from dataclasses import dataclass


@dataclass
class Settings:

    embedding_model: str = "BAAI/bge-m3"

    device: str = "cpu"

    collection_name: str = "products"

    qdrant_host: str = "localhost"

    qdrant_port: int = 6333

    top_k: int = 20