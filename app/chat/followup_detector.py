"""
Follow-up Detector

Detects whether the current user query is a follow-up
to the previous search.

Examples

Show ceiling fans
↓

Only white

↓

Under 4000

↓

Remote control

↓

BLDC

↓

Sort by price

↓

Show only Havells
"""

from __future__ import annotations

import re


FOLLOWUP_PREFIXES = (

    "only",

    "under",

    "below",

    "above",

    "over",

    "less than",

    "greater than",

    "with",

    "without",

    "having",

    "show only",

    "filter",

    "sort",

    "price",

    "brand",

    "color",

    "size",

    "capacity",

    "power",

    "remote",

    "bldc",
)


class FollowupDetector:
    """
    Detects conversational follow-up queries.
    """

    PRICE_PATTERN = re.compile(
        r"(under|below|over|above|less than|greater than)\s+\d+",
        re.I,
    )

    # ---------------------------------------------------------

    def is_followup(
        self,
        *,
        query: str,
        previous_query: str | None,
    ) -> bool:

        if not previous_query:
            return False

        query = query.strip().lower()

        if not query:
            return False

        #
        # Very short queries
        #
        if len(query.split()) <= 3:
            return True

        #
        # Starts with known follow-up words
        #
        for prefix in FOLLOWUP_PREFIXES:

            if query.startswith(prefix):
                return True

        #
        # Price modification
        #
        if self.PRICE_PATTERN.search(query):
            return True

        #
        # Contains only attribute words
        #
        if self._attribute_only(query):
            return True

        return False

    # ---------------------------------------------------------

    def merge(
        self,
        *,
        previous_query: str,
        current_query: str,
    ) -> str:
        """
        Merge follow-up into previous query.

        Example

        Ceiling fan

        +

        Only white

        ↓

        Ceiling fan only white
        """

        previous_query = previous_query.strip()

        current_query = current_query.strip()

        if not previous_query:
            return current_query

        if not current_query:
            return previous_query

        return f"{previous_query} {current_query}"

    # ---------------------------------------------------------

    def _attribute_only(
        self,
        query: str,
    ) -> bool:

        keywords = {

            "white",

            "black",

            "brown",

            "gold",

            "silver",

            "blue",

            "red",

            "green",

            "remote",

            "bldc",

            "smart",

            "wifi",

            "havells",

            "1200",

            "1400",

            "900",

            "mm",

            "star",

            "energy",

            "silent",
        }

        words = set(query.split())

        return bool(words & keywords)

    # ---------------------------------------------------------

    def explain(
        self,
        *,
        query: str,
        previous_query: str | None,
    ) -> dict:

        followup = self.is_followup(
            query=query,
            previous_query=previous_query,
        )

        merged = (
            self.merge(
                previous_query=previous_query,
                current_query=query,
            )
            if followup
            else query
        )

        return {

            "followup": followup,

            "original_query": previous_query,

            "current_query": query,

            "effective_query": merged,
        }