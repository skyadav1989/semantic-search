"""
Search Context

Carries the complete state of a search request through the
entire search pipeline.

Every pipeline stage reads and updates this object.

QueryProcessor
      ↓
QueryExpander
      ↓
FilterBuilder
      ↓
Embedder
      ↓
Retriever
      ↓
Reranker
      ↓
BusinessRanker
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SearchContext:
    """
    Shared object passed through the complete search pipeline.
    """

    # -------------------------------------------------------
    # Request
    # -------------------------------------------------------

    query: str

    limit: int = 20

    filters: dict[str, Any] = field(default_factory=dict)

    options: dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------
    # Query Processing
    # -------------------------------------------------------

    normalized_query: str = ""

    expanded_query: str = ""

    expanded_terms: list[str] = field(default_factory=list)

    intent: str | None = None

    attributes: dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------
    # Embedding
    # -------------------------------------------------------

    query_embedding: list[float] | None = None

    # -------------------------------------------------------
    # Retrieval
    # -------------------------------------------------------

    candidates: list[dict] = field(default_factory=list)

    # -------------------------------------------------------
    # Reranking
    # -------------------------------------------------------

    reranked_results: list[dict] = field(default_factory=list)

    # -------------------------------------------------------
    # Final Results
    # -------------------------------------------------------

    results: list[dict] = field(default_factory=list)

    # -------------------------------------------------------
    # Diagnostics
    # -------------------------------------------------------

    elapsed_ms: float = 0.0

    debug: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------

    def add_debug(self, key: str, value: Any) -> None:
        """
        Store debugging information.
        """

        self.debug[key] = value

    def set_embedding(self, vector: list[float]) -> None:
        """
        Store query embedding.
        """

        self.query_embedding = vector

    def set_candidates(
        self,
        candidates: list[dict],
    ) -> None:
        """
        Store retrieved candidates.
        """

        self.candidates = candidates

    def set_reranked(
        self,
        results: list[dict],
    ) -> None:
        """
        Store reranked results.
        """

        self.reranked_results = results

    def set_results(
        self,
        results: list[dict],
    ) -> None:
        """
        Store final results.
        """

        self.results = results

    def to_dict(self) -> dict:
        """
        Serialize context.
        """

        return {
            "query": self.query,
            "normalized_query": self.normalized_query,
            "expanded_query": self.expanded_query,
            "expanded_terms": self.expanded_terms,
            "intent": self.intent,
            "attributes": self.attributes,
            "results": self.results,
            "elapsed_ms": self.elapsed_ms,
            "metadata": self.metadata,
        }