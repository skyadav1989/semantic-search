"""
Recommendation Business Rules

Applies business constraints before and after semantic ranking.
"""

from __future__ import annotations

from .constants import (
    PRICE_VARIATION_PERCENT,
)


class BusinessRuleEngine:
    """
    Applies business rules to recommendation candidates.
    """

    # ---------------------------------------------------------

    def apply(
        self,
        *,
        source: dict,
        candidates: list[dict],
    ) -> list[dict]:

        filtered = []

        for candidate in candidates:

            if not self._is_valid(
                source,
                candidate,
            ):
                continue

            candidate["business_score"] = self.score(
                source,
                candidate,
            )

            filtered.append(candidate)

        return filtered

    # ---------------------------------------------------------

    def _is_valid(
        self,
        source: dict,
        candidate: dict,
    ) -> bool:
        """
        Validate candidate.
        """

        source_payload = source.get("payload", {})
        candidate_payload = candidate.get("payload", {})

        #
        # Exclude same product
        #
        if (
            source_payload.get("sku")
            == candidate_payload.get("sku")
        ):
            return False

        #
        # Stock
        #
        if (
            candidate_payload.get("stock_status")
            != "In stock"
        ):
            return False

        #
        # Price
        #
        source_price = source_payload.get("price")

        candidate_price = candidate_payload.get("price")

        if source_price and candidate_price:

            variation = (
                source_price
                * PRICE_VARIATION_PERCENT
                / 100
            )

            if (
                candidate_price
                < source_price - variation
            ):
                return False

            if (
                candidate_price
                > source_price + variation
            ):
                return False

        return True

    # ---------------------------------------------------------

    def score(
        self,
        source: dict,
        candidate: dict,
    ) -> float:
        """
        Calculate business score.
        """

        score = 0.0

        source_payload = source.get("payload", {})
        candidate_payload = candidate.get("payload", {})

        #
        # Same Category
        #
        if (
            source_payload.get("category")
            == candidate_payload.get("category")
        ):
            score += 0.30

        #
        # Same Subcategory
        #
        if (
            source_payload.get("subcategory")
            == candidate_payload.get("subcategory")
        ):
            score += 0.30

        #
        # Same Brand
        #
        if (
            source_payload.get("brand")
            and source_payload.get("brand")
            == candidate_payload.get("brand")
        ):
            score += 0.20

        #
        # In Stock
        #
        if (
            candidate_payload.get("stock_status")
            == "In stock"
        ):
            score += 0.20

        return round(score, 4)