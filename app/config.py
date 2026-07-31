from jinja2 import environment
from functools import lru_cache
import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class Settings(BaseModel):
    """
    Application configuration loaded from .env and process environment.
    """

    model_config = ConfigDict(extra="ignore")

    # Search Mode
    SEARCH_MODE: str = "hybrid"

    # Feature Flags
    ENABLE_SEMANTIC: bool = True
    ENABLE_BM25: bool = True
    ENABLE_RRF: bool = True
    ENABLE_QUERY_EXPANSION: bool = True
    ENABLE_RERANKER: bool = False
    ENABLE_BUSINESS_RANKING: bool = True

    # Retrieval
    SEMANTIC_LIMIT: int = 20
    BM25_LIMIT: int = 20
    FINAL_RESULTS: int = 10

    # Embedding
    EMBEDDING_MODEL: str = "BAAI/bge-m3"
    EMBEDDING_DEVICE: str = "cpu"

    # Reranker
    RERANKER_MODEL: str = "BAAI/bge-reranker-base"

    # Qdrant
    QDRANT_URL: str | None = None
    QDRANT_API_KEY: str | None = None
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: int = 6334
    QDRANT_COLLECTION: str = "products"

    ENABLE_FACETS = True

    FACET_LIMIT = 10

    ENABLE_FACETS: bool = True

    FACET_LIMIT: int = 10

    #
    # LLM
    #
    LLM_PROVIDER: str = "gemini"

    LLM_MODEL: str = "gemini-2.5-flash"

    GEMINI_API_KEY: str = ""

    OPENAI_API_KEY: str = ""

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    ENABLE_LLM: bool = True

    MAX_CONTEXT_PRODUCTS: int = 10


    @property
    def qdrant_url(self) -> str:
        if self.QDRANT_URL:
            return self.QDRANT_URL
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"


def _load_env_file() -> None:
    env_file = Path(".env")

    if load_dotenv is not None:
        load_dotenv(env_file)
        return

    if not env_file.exists():
        return

    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@lru_cache
def get_settings() -> Settings:
    _load_env_file()
    values = {
        key: os.environ[key]
        for key in Settings.model_fields
        if key in os.environ
    }
    return Settings(**values)
