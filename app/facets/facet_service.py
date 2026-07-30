"""
Facet Service

Facade over the complete Facet Engine.

SearchService should only call this class.
"""

from __future__ import annotations

import logging

from .facet_builder import FacetBuilder
from .response_builder import FacetResponseBuilder

logger = logging.getLogger(__name__)


class FacetService:
    """
    Facade for generating search facets.

    Responsibilities

    - Build facets
    - Format response
    - Hide implementation details
    """

    def __init__(self):

        self.builder = FacetBuilder()

        self.response = FacetResponseBuilder()

    # ---------------------------------------------------------

    def generate(
        self,
        results: list[dict],
    ) -> dict:

        logger.info(
            "Generating facets from %d products",
            len(results),
        )

        facets = self.builder.build(results)

        return self.response.build(facets)