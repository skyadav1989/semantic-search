"""
Search Service

Application service responsible for executing
the complete semantic search workflow.

Flow

Query
    ↓
QueryProcessor
    ↓
QueryExpander
    ↓
Metadata Filter Builder
    ↓
BGEM3 Embedder
    ↓
Qdrant Retriever
    ↓
CrossEncoder Reranker
    ↓
Business Ranker
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class SearchService:

    def __init__(
        self,
        *,
        query_processor,
        query_expander,
        filter_builder,
        embedder,
        retriever,
        reranker,
        business_ranker,
    ):
        self.query_processor = query_processor
        self.query_expander = query_expander
        self.filter_builder = filter_builder
        self.embedder = embedder
        self.retriever = retriever
        self.reranker = reranker
        self.business_ranker = business_ranker

    # ------------------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = 20,
        **kwargs: Any,
    ) -> dict:

        started = time.perf_counter()

        logger.info("Search query: %s", query)

        #
        # 1. Process Query
        #
        processed = self.query_processor.process(query)

        normalized_query = processed["normalized_query"]

        attributes = processed["attributes"]

        metadata_filter = self.filter_builder.build(
            attributes
        )

        #
        # 2. Expand Query
        #
        expanded = self.query_expander.expand(
            normalized_query
        )

        expanded_query = expanded["expanded_query"]

        expanded_terms = expanded["expanded_terms"]

        #
        # 3. Create Embedding
        #
        vector = self.embedder.encode_query(
            expanded_query
        )

        #
        # 4. Retrieve
        #
        candidates = self.retriever.retrieve(
            vector,
            limit=limit,
            metadata_filter=metadata_filter,
        )

        #
        # 5. AI Rerank
        #
        reranked = self.reranker.rerank(
            expanded_query,
            candidates,
            top_k=limit,
        )

        #
        # 6. Business Ranking
        #
        results = self.business_ranker.rank(
            reranked
        )

        elapsed = round(
            (time.perf_counter() - started) * 1000,
            2,
        )

        return {
            "query": query,
            "normalized_query": normalized_query,
            "expanded_query": expanded_query,
            "expanded_terms": expanded_terms,
            "intent": processed["intent"],
            "filters": attributes,
            "count": len(results),
            "elapsed_ms": elapsed,
            "results": results,
        }