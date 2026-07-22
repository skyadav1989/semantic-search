"""
BGE-M3 Embedder

Production wrapper around SentenceTransformer.

Features
--------
- Singleton friendly
- Query encoding
- Batch encoding
- Device support
- Configurable batch size
- Logging
"""

from __future__ import annotations

import logging
from typing import Iterable

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


logger = logging.getLogger(__name__)


class BGEM3Embedder:

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: str = "cpu",
        batch_size: int = 32,
        normalize: bool = True,
    ):

        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers is not installed."
            )

        logger.info(
            "Loading embedding model %s",
            model_name,
        )

        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.normalize = normalize

        self.model = SentenceTransformer(
            model_name,
            device=device,
        )

        logger.info("Embedding model loaded.")

    # --------------------------------------------------

    def encode(
        self,
        text: str,
    ) -> list[float]:
        """
        Encode a single query/document.
        """

        if not text:
            return []

        return self.model.encode(
            text,
            normalize_embeddings=self.normalize,
        ).tolist()

    # --------------------------------------------------

    def encode_batch(
        self,
        texts: Iterable[str],
    ) -> list[list[float]]:
        """
        Encode multiple texts.
        """

        texts = list(texts)

        if not texts:
            return []

        vectors = self.model.encode(
            texts,
            normalize_embeddings=self.normalize,
            batch_size=self.batch_size,
            show_progress_bar=False,
        )

        return vectors.tolist()

    # --------------------------------------------------

    def encode_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Alias for semantic search.
        """

        return self.encode(query)

    # --------------------------------------------------

    def encode_document(
        self,
        document: str,
    ) -> list[float]:
        """
        Alias for indexing.
        """

        return self.encode(document)

    # --------------------------------------------------

    @property
    def dimension(self) -> int:
        """
        Vector dimension.
        """

        return self.model.get_sentence_embedding_dimension()

    # --------------------------------------------------

    def __repr__(self):

        return (
            f"BGEM3Embedder("
            f"model='{self.model_name}', "
            f"device='{self.device}')"
        )