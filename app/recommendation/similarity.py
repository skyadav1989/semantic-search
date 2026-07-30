"""
Recommendation Similarity Engine

Responsible for calculating similarity between
source product and candidate product.
"""

from __future__ import annotations

from .constants import (
    SEMANTIC_WEIGHT,
    BUSINESS_WEIGHT,
    STOCK_WEIGHT,
    PRICE_WEIGHT,
)

from .utils import (
    price_similarity,
    merge_scores,
)


class SimilarityEngine:
    """
    Computes recommendation score.

    Final Score =
        Semantic +
        Business +
        Stock +
        Price
    """

    def score(
        self,
        *,
        source: dict,
        candidate: dict,
    ):

        source_payload = source.get("payload", {})
        candidate_payload = candidate.get("payload", {})

        #
        # Semantic Score
        #
        semantic_score = float(
            candidate.get("score", 0)
        )

        #
        # Business Score
        #
        business_score = float(
            candidate.get(
                "business_score",
                0,
            )
        )

        #
        # Stock Score
        #
        stock_score = (
            1.0
            if candidate_payload.get(
                "stock_status"
            ) == "In stock"
            else 0.0
        )

        #
        # Price Score
        #
        price_score = price_similarity(
            float(
                source_payload.get(
                    "price",
                    0,
                )
            ),
            float(
                candidate_payload.get(
                    "price",
                    0,
                )
            ),
        )

        return merge_scores(
            semantic=semantic_score,
            business=business_score,
            stock=stock_score,
            price=price_score,
            semantic_weight=SEMANTIC_WEIGHT,
            business_weight=BUSINESS_WEIGHT,
            stock_weight=STOCK_WEIGHT,
            price_weight=PRICE_WEIGHT,
        )

    # ---------------------------------------------------------

    def rank(
        self,
        *,
        source: dict,
        candidates: list[dict],
    ) -> list[dict]:
        """
        Score every candidate.
        """

        ranked = []

        for candidate in candidates:

            recommendation_score = self.score(
                source=source,
                candidate=candidate,
            )

            candidate["recommendation_score"] = (
                recommendation_score
            )

            ranked.append(candidate)

        ranked.sort(
            key=lambda x: x[
                "recommendation_score"
            ].final,
            reverse=True,
        )

        return ranked