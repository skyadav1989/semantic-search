"""
Search Pipeline

Coordinates the complete semantic search workflow.

The pipeline itself contains no business logic. Each component
is responsible for one task.

Flow

Query
  ↓
QueryProcessor
  ↓
QueryExpander
  ↓
FilterBuilder
  ↓
Retriever
  ↓
Reranker
  ↓
BusinessRanker
"""

from __future__ import annotations

import logging
import time
from typing import Any

from app.search.search_context import SearchContext

logger = logging.getLogger(__name__)


class SearchPipeline:
    """
    Executes the complete search workflow.
    """

    def __init__(
        self,
        query_processor,
        query_expander,
        filter_builder,
        retriever,
        reranker,
        business_ranker,
    ):
        self.query_processor = query_processor
        self.query_expander = query_expander
        self.filter_builder = filter_builder
        self.retriever = retriever
        self.reranker = reranker
        self.business_ranker = business_ranker

    # ---------------------------------------------------------

    def run(
        self,
        query: str,
        limit: int = 20,
        **options: Any,
    ) -> dict:
        """
        Execute search pipeline.
        """

        context = SearchContext(
            query=query,
            limit=limit,
            options=options,
        )

        started = time.perf_counter()

        try:

            self.process_query(context)

            self.expand_query(context)

            self.build_filters(context)

            self.retrieve(context)

            self.rerank(context)

            self.apply_business_rules(context)

            context.elapsed_ms = round(
                (time.perf_counter() - started) * 1000,
                2,
            )

            return context.to_dict()

        except Exception:

            logger.exception(
                "Search pipeline failed."
            )

            raise

    # ---------------------------------------------------------

    def process_query(
        self,
        context: SearchContext,
    ) -> None:

        result = self.query_processor.process(
            context.query
        )

        context.normalized_query = result.get(
            "normalized_query",
            context.query,
        )

        context.intent = result.get(
            "intent"
        )

        context.attributes = result.get(
            "attributes",
            {},
        )

    # ---------------------------------------------------------

    def expand_query(
        self,
        context: SearchContext,
    ) -> None:

        result = self.query_expander.expand(
            context.normalized_query
        )

        context.expanded_query = result.get(
            "expanded_query",
            context.normalized_query,
        )

        context.expanded_terms = result.get(
            "expanded_terms",
            [],
        )

    # ---------------------------------------------------------

    def build_filters(
        self,
        context: SearchContext,
    ) -> None:

        context.filters = self.filter_builder.build(
            context.attributes
        )

    # ---------------------------------------------------------

    def retrieve(
        self,
        context: SearchContext,
    ) -> None:

        candidates = self.retriever.retrieve(
            query=context.expanded_query,
            metadata_filter=context.filters,
            limit=context.limit,
        )

        context.set_candidates(candidates)

    # ---------------------------------------------------------

    def rerank(
        self,
        context: SearchContext,
    ) -> None:

        reranked = self.reranker.rerank(
            context.expanded_query,
            context.candidates,
            top_k=context.limit,
        )

        context.set_reranked(reranked)

    # ---------------------------------------------------------

    def apply_business_rules(
        self,
        context: SearchContext,
    ) -> None:

        results = self.business_ranker.rank(
            context.reranked_results
        )

        context.set_results(results)