"""
Recommendation Query Builder

Builds recommendation queries from a source product.
"""

from __future__ import annotations

from .constants import (
    DEFAULT_LIMIT,
    MAX_LIMIT,
)


class RecommendationQueryBuilder:
    """
    Builds recommendation queries for Qdrant retrieval.
    """

    def build(
        self,
        *,
        source_product: dict,
        recommendation_type: str,
        limit: int = DEFAULT_LIMIT,
    ) -> dict:

        payload = source_product.get("payload", {})

        return {
            "sku": payload.get("sku"),
            "vector": source_product.get("vector"),
            "category": payload.get("category"),
            "subcategory": payload.get("subcategory"),
            "brand": payload.get("brand"),
            "price": payload.get("price"),
            "attributes": payload.get("attributes", {}),
            "recommendation_type": recommendation_type,
            "limit": min(limit, MAX_LIMIT),
        }

    # ---------------------------------------------------------

    def build_filter(
        self,
        recommendation: dict,
    ) -> dict:
        """
        Build metadata filters for recommendation search.
        """

        filters = {}

        #
        # Keep recommendations in same category
        #
        if recommendation.get("category"):
            filters["category"] = recommendation["category"]

        #
        # Alternatives should stay in same subcategory
        #
        if (
            recommendation["recommendation_type"] == "alternative"
            and recommendation.get("subcategory")
        ):
            filters["subcategory"] = recommendation["subcategory"]

        return filters

    # ---------------------------------------------------------

    def exclude_source_sku(
        self,
        candidates: list[dict],
        sku: str,
    ) -> list[dict]:
        """
        Remove source product from recommendations.
        """

        return [
            candidate
            for candidate in candidates
            if candidate.get("payload", {}).get("sku") != sku
        ]
