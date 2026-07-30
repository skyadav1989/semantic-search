"""
Recommendation Strategy

Defines recommendation generation strategies.
"""

from __future__ import annotations

from .enums import RecommendationType


class RecommendationStrategy:
    """
    Applies strategy-specific filtering and ranking.
    """

    # ---------------------------------------------------------

    def apply(
        self,
        *,
        recommendation_type: str,
        source: dict,
        candidates: list[dict],
    ) -> list[dict]:

        if recommendation_type == RecommendationType.SIMILAR:
            return self.similar(
                source=source,
                candidates=candidates,
            )

        if recommendation_type == RecommendationType.ALTERNATIVE:
            return self.alternative(
                source=source,
                candidates=candidates,
            )

        if recommendation_type == RecommendationType.COMPLEMENTARY:
            return self.complementary(
                source=source,
                candidates=candidates,
            )

        if recommendation_type == RecommendationType.TRENDING:
            return self.trending(
                candidates=candidates,
            )

        return candidates

    # ---------------------------------------------------------

    def similar(
        self,
        *,
        source: dict,
        candidates: list[dict],
    ) -> list[dict]:
        """
        Similar products.

        Same category + highest semantic score.
        """

        category = source["payload"].get("category")

        return [
            c
            for c in candidates
            if c["payload"].get("category") == category
        ]

    # ---------------------------------------------------------

    def alternative(
        self,
        *,
        source: dict,
        candidates: list[dict],
    ) -> list[dict]:
        """
        Alternatives.

        Same category
        Same subcategory
        Different SKU
        """

        payload = source["payload"]

        category = payload.get("category")
        subcategory = payload.get("subcategory")
        sku = payload.get("sku")

        return [

            c

            for c in candidates

            if (
                c["payload"].get("category") == category
                and
                c["payload"].get("subcategory") == subcategory
                and
                c["payload"].get("sku") != sku
            )
        ]

    # ---------------------------------------------------------

    def complementary(
        self,
        *,
        source: dict,
        candidates: list[dict],
    ) -> list[dict]:
        """
        Complementary products.

        Placeholder.

        Future:
            YAML
            AI
            Rule Engine
        """

        return candidates

    # ---------------------------------------------------------

    def trending(
        self,
        *,
        candidates: list[dict],
    ) -> list[dict]:
        """
        Trending products.

        Sorted by business score.
        """

        return sorted(
            candidates,
            key=lambda x: x.get(
                "business_score",
                0,
            ),
            reverse=True,
        )