"""
Search Service

Application service responsible for executing the configured product search workflow.
"""
from __future__ import annotations
from jinja2 import filters
import logging
from app.facets.facet_service import FacetService
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
        hybrid_retriever,
        rrf,
        reranker,
        business_ranker,
        facet_service: FacetService | None = None,  
        settings,
        enable_semantic: bool,
        enable_bm25: bool,
        enable_rrf: bool,
        enable_query_expansion: bool,
        enable_business_ranking: bool,
    ):
        self.query_processor = query_processor
        self.query_expander = query_expander
        self.filter_builder = filter_builder
        self.embedder = embedder
        self.hybrid_retriever = hybrid_retriever
        self.rrf = rrf
        self.reranker = reranker
        self.business_ranker = business_ranker
        self.facet_service = facet_service
        self.settings = settings
        self.enable_semantic = enable_semantic
        self.enable_bm25 = enable_bm25
        self.enable_rrf = enable_rrf
        self.enable_query_expansion = enable_query_expansion
        self.enable_business_ranking = enable_business_ranking

    # ------------------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = 20,
        **kwargs: Any,
    ) -> dict:

        started = time.perf_counter()

        if not self.enable_semantic and not self.enable_bm25:
            raise ValueError(
                "No retrieval backend is enabled. "
                "Set SEARCH_MODE to semantic, bm25, or hybrid."
            )

        final_limit = min(limit, self.settings.FINAL_RESULTS)
        semantic_limit = max(final_limit, self.settings.SEMANTIC_LIMIT)
        bm25_limit = max(final_limit, self.settings.BM25_LIMIT)

        logger.info("=" * 80)
        logger.info("Search Query : %s", query)
        logger.info("Search Mode  : %s", self.settings.SEARCH_MODE)

        logger.info("Feature Flags")
        logger.info("  Semantic Search    : %s", "ENABLED" if self.enable_semantic else "DISABLED")
        logger.info("  BM25 Search        : %s", "ENABLED" if self.enable_bm25 else "DISABLED")
        logger.info("  RRF Fusion         : %s", "ENABLED" if self.enable_rrf else "DISABLED")
        logger.info("  Query Expansion    : %s", "ENABLED" if self.enable_query_expansion else "DISABLED")
        logger.info("  Cross Encoder      : %s", "ENABLED" if self.reranker else "DISABLED")
        logger.info("  Business Ranking   : %s", "ENABLED" if self.enable_business_ranking else "DISABLED")
        logger.info(
            "  Facet Engine       : %s",
            "ENABLED"
            if getattr(self.settings, "ENABLE_FACETS", False)
            else "DISABLED",
        )
        logger.info("=" * 80)

        #
        # Query Processing
        #
        processed = self.query_processor.process(query)

        normalized_query = processed["normalized_query"]

        attributes = processed.get("attributes", {})

        filters = processed.get("filters", {})

        #
        # Backward compatibility
        #
        if not filters:
            if "max_price" in attributes:
                filters["max_price"] = attributes["max_price"]

            if "min_price" in attributes:
                filters["min_price"] = attributes["min_price"]

            if "category" in attributes:
                filters["category"] = attributes["category"]

            if "subcategory" in attributes:
                filters["subcategory"] = attributes["subcategory"]

            if "brand" in attributes:
                filters["brand"] = attributes["brand"]

            if "color" in attributes:
                filters["color"] = attributes["color"]

        #
        # Build Qdrant Metadata Filter
        #
        metadata_filter = self.filter_builder.build(filters)

        logger.info("Query Attributes : %s", attributes)
        logger.info("Query Filters    : %s", filters)
        logger.info("Metadata Filter  : %s", metadata_filter)

        #
        # Query Expansion
        #
        if self.enable_query_expansion:

            expanded = self.query_expander.expand(normalized_query)

            expanded_query = expanded["expanded_query"]

            expanded_terms = expanded["expanded_terms"]

        else:

            expanded_query = normalized_query

            expanded_terms = []

        #
        # Embedding
        #
        vector = None

        if self.enable_semantic:
            vector = self.embedder.encode_query(expanded_query)

        #
        # Retrieval
        #
        retrieved = self.hybrid_retriever.retrieve(
            vector=vector,
            query=expanded_query,
            metadata_filter=metadata_filter,
            semantic_limit=semantic_limit,
            bm25_limit=bm25_limit,
            enable_semantic=self.enable_semantic,
            enable_bm25=self.enable_bm25,
        )

        semantic_results = retrieved["semantic"]

        bm25_results = retrieved["bm25"]

        #
        # Merge
        #
        if self.enable_semantic and self.enable_bm25:

            if self.enable_rrf:

                candidates = self.rrf.fuse(
                    semantic_results,
                    bm25_results,
                    top_k=max(final_limit * 2, final_limit),
                )

            else:

                candidates = self._merge_ranked(
                    semantic_results,
                    bm25_results,
                    top_k=max(final_limit * 2, final_limit),
                )

        elif self.enable_semantic:

            candidates = semantic_results[:final_limit]

        else:

            candidates = bm25_results[:final_limit]

        #
        # Cross Encoder
        #
        if self.reranker:

            candidates = self.reranker.rerank(
                expanded_query,
                candidates,
                top_k=final_limit,
            )

            for item in candidates:

                if "cross_score" in item:
                    item["rerank_score"] = item["cross_score"]

        else:

            candidates = candidates[:final_limit]

        #
        # Business Ranking
        #
        if self.enable_business_ranking and self.business_ranker:

            results = self.business_ranker.rank(candidates)[:final_limit]

        else:

            results = candidates[:final_limit]

        #
        # Generate Facets
        #
        facets = {}

        if (
            getattr(self.settings, "ENABLE_FACETS", False)
            and self.facet_service is not None
        ):

            try:

                facets = self.facet_service.generate(results)

                logger.info(
                    "Facet Engine Generated : %d groups",
                    len(facets),
                )

            except Exception:

                logger.exception(
                    "Facet generation failed"
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

            #
            # Query Understanding
            #
            "attributes": attributes,
            "filters": filters,

            #
            # Search Config
            #
            "search_mode": self.settings.SEARCH_MODE,

            "features": {
                "semantic": self.enable_semantic,
                "bm25": self.enable_bm25,
                "rrf": self.enable_rrf,
                "query_expansion": self.enable_query_expansion,
                "reranker": self.reranker is not None,
                "business_ranking": self.enable_business_ranking,
            },

            "count": len(results),

            "elapsed_ms": elapsed,
            "facets": facets,

            "results": results,
        }

    # ------------------------------------------------------------

    def _merge_ranked(self, *result_sets, top_k: int) -> list[dict]:

        merged = {}

        for results in result_sets:

            for item in results:

                payload = item.get("payload", {})

                key = payload.get("sku") or item.get("id")

                if key is None:
                    continue

                previous = merged.get(key)

                if (
                    previous is None
                    or item.get("score", 0)
                    > previous.get("score", 0)
                ):
                    merged[key] = item

        return sorted(
            merged.values(),
            key=lambda item: item.get(
                "score",
                item.get("rrf_score", 0),
            ),
            reverse=True,
        )[:top_k]