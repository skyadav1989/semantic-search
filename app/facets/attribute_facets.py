"""
Attribute Facet Builder

Generates dynamic facets from product attributes.

No hardcoded product fields.

Works for

Fans
TV
AC
Laptop
Furniture
etc.
"""

from __future__ import annotations

import logging
from collections import Counter

from .constants import (
    IGNORE_ATTRIBUTES,
    FACET_LIMIT,
)
from .utils import (
    increment,
    counter_to_facet,
)

logger = logging.getLogger(__name__)


class AttributeFacetBuilder:
    """
    Dynamic Attribute Facet Generator.
    """

    def __init__(
        self,
        ignored_attributes: set[str] | None = None,
        limit: int = FACET_LIMIT,
    ):

        self.ignored = (
            ignored_attributes
            or IGNORE_ATTRIBUTES
        )

        self.limit = limit

    # ---------------------------------------------------------

    def build(
        self,
        results: list[dict],
    ) -> dict:
        """
        Build all attribute facets.

        Returns

        {
            "body_colour":[...],
            "sweep_size":[...],
            "power_consumption":[...]
        }
        """

        counters: dict[str, Counter] = {}

        for item in results:

            payload = item.get("payload", {})

            attributes = (
                payload.get("attributes")
                or {}
            )

            if not attributes:
                continue

            for key, value in attributes.items():

                if key in self.ignored:
                    continue

                #
                # Skip empty values
                #

                if value in (
                    None,
                    "",
                    [],
                    {},
                ):
                    continue

                #
                # List values
                #

                if isinstance(value, list):

                    for v in value:

                        increment(
                            counters.setdefault(
                                key,
                                Counter(),
                            ),
                            v,
                        )

                    continue

                #
                # String / Number
                #

                increment(
                    counters.setdefault(
                        key,
                        Counter(),
                    ),
                    value,
                )

        #
        # Convert Counter → FacetValue
        #

        facets = {}

        for key, counter in counters.items():

            values = counter_to_facet(
                counter,
                limit=self.limit,
            )

            if values:
                facets[key] = values

        logger.info(
            "Generated %d attribute facets",
            len(facets),
        )

        return facets