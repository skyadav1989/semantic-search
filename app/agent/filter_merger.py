"""
Filter Merger

Merges conversational filters.

Example

User:
Best ceiling fan under 5000

↓

filters

{
    "category":"Ceiling Fan",
    "max_price":5000
}

↓

User:
Only BLDC

↓

{
    "category":"Ceiling Fan",
    "max_price":5000,
    "motor":"BLDC"
}
"""

from __future__ import annotations

import re

from .memory import ConversationMemory


class FilterMerger:

    # ---------------------------------------------------------

    def merge(
        self,
        memory: ConversationMemory,
        query: str,
    ) -> dict:
        """
        Merge previous filters with the current query.
        """

        filters = dict(memory.filters)

        query_lower = query.lower()

        #
        # Brand
        #

        brands = [
            "havells",
            "lloyd",
            "standard",
            "crabtree",
        ]

        for brand in brands:

            if brand in query_lower:

                filters["brand"] = brand.title()

        #
        # Motor
        #

        if "bldc" in query_lower:

            filters["motor"] = "BLDC"

        #
        # Remote
        #

        if "remote" in query_lower:

            filters["remote"] = True

        #
        # Color
        #

        colors = [
            "white",
            "black",
            "brown",
            "ivory",
            "gold",
        ]

        for color in colors:

            if color in query_lower:

                filters["color"] = color

        #
        # Budget
        #

        m = re.search(
            r"under\s+(\d+)",
            query_lower,
        )

        if m:

            filters["max_price"] = int(
                m.group(1),
            )

        #
        # Remove Brand
        #

        if "remove" in query_lower:

            for brand in brands:

                if brand in query_lower:

                    if filters.get("brand") == brand.title():

                        filters.pop(
                            "brand",
                            None,
                        )

        return filters

    # ---------------------------------------------------------

    def update_memory(
        self,
        memory: ConversationMemory,
        filters: dict,
    ) -> None:

        memory.filters = filters