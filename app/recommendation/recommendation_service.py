"""
Recommendation Service

Enterprise recommendation engine.

Flow

SKU
 ↓
Load Source Product
 ↓
Retrieve Candidates
 ↓
Business Rules
 ↓
Strategy
 ↓
Similarity Ranking
 ↓
Response
"""

from __future__ import annotations

import logging

from .constants import DEFAULT_LIMIT
from .query_builder import RecommendationQueryBuilder
from .business_rules import BusinessRuleEngine
from .strategy import RecommendationStrategy
from .similarity import SimilarityEngine
from .exceptions import ProductNotFoundError
from app.search.filter_builder import MetadataFilterBuilder

logger = logging.getLogger(__name__)


class RecommendationService:
    """
    Recommendation Engine
    """

    def __init__(
        self,
        *,
        retriever,
        filter_builder: MetadataFilterBuilder,
        query_builder: RecommendationQueryBuilder,
        business_rules: BusinessRuleEngine,
        strategy: RecommendationStrategy,
        similarity: SimilarityEngine,
    ):
        self.retriever = retriever
        self.query_builder = query_builder
        self.business_rules = business_rules
        self.strategy = strategy
        self.similarity = similarity
        self.filter_builder = filter_builder
        

    # ---------------------------------------------------------

    def recommend(
        self,
        *,
        sku: str,
        recommendation_type: str = "similar",
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict]:
        """
        Generate recommendations.
        """

        logger.info(
            "Generating %s recommendations",
            recommendation_type,
        )

        source_product = self.retriever.get_by_sku(sku)

        if source_product is None:
            raise ProductNotFoundError(
                f"Product '{sku}' not found."
            )

        logger.info(
            "Loaded source product : %s",
            sku,
        )

        #
        # Build Recommendation Query
        #
        recommendation = self.query_builder.build(
            source_product=source_product,
            recommendation_type=recommendation_type,
            limit=limit,
        )

        #
        # Build Metadata Filter
        #
        filters = self.query_builder.build_filter(
            recommendation
        )

        metadata_filter = self.filter_builder.build(filters)

        logger.info(
            "Recommendation Filters : %s",
            filters,
        )

        logger.info(
            "Metadata Filter : %s",
            metadata_filter,
        )

        #
        # Retrieve Semantic Candidates
        #
        candidates = self.retriever.retrieve(
            vector=recommendation["vector"],
            limit=limit * 3,
            metadata_filter=metadata_filter,
        )

        logger.info(
            "Retrieved %d candidates",
            len(candidates),
        )

        #
        # Remove Source SKU
        #
        candidates = self.query_builder.exclude_source_sku(
            candidates,
            recommendation["sku"],
        )

        #
        # Apply Business Rules
        #
        candidates = self.business_rules.apply(
            source=source_product,
            candidates=candidates,
        )

        logger.info(
            "Business Rule Candidates : %d",
            len(candidates),
        )

        #
        # Strategy
        #
        candidates = self.strategy.apply(
            recommendation_type=recommendation_type,
            source=source_product,
            candidates=candidates,
        )

        logger.info(
            "Strategy Candidates : %d",
            len(candidates),
        )

        #
        # Similarity Ranking
        #
        candidates = self.similarity.rank(
            source=source_product,
            candidates=candidates,
        )

        logger.info(
            "Final Recommendations : %d",
            len(candidates),
        )

        logger.info(
            "Recommendation completed for SKU %s",
            sku,
        )

        return candidates[:limit]

    # ---------------------------------------------------------

    def similar(
        self,
        *,
        sku: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict]:

        return self.recommend(
            sku=sku,
            recommendation_type="similar",
            limit=limit,
        )

    # ---------------------------------------------------------

    def alternatives(
        self,
        *,
        sku: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict]:

        return self.recommend(
            sku=sku,
            recommendation_type="alternative",
            limit=limit,
        )

    # ---------------------------------------------------------

    def complementary(
        self,
        *,
        sku: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict]:

        return self.recommend(
            sku=sku,
            recommendation_type="complementary",
            limit=limit,
        )

    # ---------------------------------------------------------

    def trending(
        self,
        *,
        sku: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict]:

        return self.recommend(
            sku=sku,
            recommendation_type="trending",
            limit=limit,
        )