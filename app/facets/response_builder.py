"""
Facet Response Builder

Formats the final API response for the frontend.

This class is responsible ONLY for formatting.
No facet generation happens here.
"""

from __future__ import annotations

from typing import Any


class FacetResponseBuilder:
    """
    Converts internal facet objects into API response.
    """

    # ---------------------------------------------------------

    def build(
        self,
        facets: dict[str, list],
    ) -> dict[str, Any]:

        response = {}

        for facet_name, values in facets.items():

            if not values:
                continue

            response[facet_name] = [
                {
                    "value": item.value,
                    "count": item.count,
                }
                for item in values
            ]

        return response