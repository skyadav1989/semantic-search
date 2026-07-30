"""
Price Bucket Builder

Converts product prices into configurable price buckets.

Example

Price:
2199

↓

Bucket:
2000-3000
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class PriceBucketBuilder:
    """
    Generic Price Bucket Generator.

    Buckets can be configured from .env

    Example

    PRICE_BUCKETS=0-1000,1000-2000,2000-3000,3000-5000,5000+
    """

    def __init__(
        self,
        buckets: list[tuple[int, int | None]] | None = None,
    ):

        #
        # Default buckets
        #

        self.buckets = buckets or [
            (0, 1000),
            (1000, 2000),
            (2000, 3000),
            (3000, 5000),
            (5000, None),
        ]

    # ---------------------------------------------------------

    def bucket(self, price) -> str | None:
        """
        Return bucket label.

        Examples

        899
            -> 0-1000

        2499
            -> 2000-3000

        7200
            -> 5000+
        """

        if price is None:
            return None

        try:
            price = float(price)
        except (TypeError, ValueError):
            return None

        for minimum, maximum in self.buckets:

            #
            # Last bucket
            #

            if maximum is None:

                if price >= minimum:
                    return f"{minimum}+"

                continue

            if minimum <= price < maximum:
                return f"{minimum}-{maximum}"

        return None

    # ---------------------------------------------------------

    def build(
        self,
        results: list[dict],
    ) -> dict[str, int]:
        """
        Build price facet.

        Returns

        {
            "0-1000":12,
            "1000-2000":8
        }
        """

        buckets: dict[str, int] = {}

        for item in results:

            payload = item.get("payload", {})

            label = self.bucket(
                payload.get("price")
            )

            if label is None:
                continue

            buckets[label] = (
                buckets.get(label, 0) + 1
            )

        logger.debug(
            "Generated %d price buckets",
            len(buckets),
        )

        return buckets