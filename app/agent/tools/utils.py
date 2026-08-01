"""
Search Tool

Delegates product search to the SearchService.
"""

from __future__ import annotations

import logging

from app.agent.models import ExecutionContext

logger = logging.getLogger(__name__)


class SearchTool:

    def __init__(
        self,
        *,
        search_service,
    ):
        self.search_service = search_service

    # ---------------------------------------------------------

    def execute(
        self,
        *,
        context: ExecutionContext,
        query: str,
        limit: int = 10,
        **_,
    ) -> dict:

        logger.info(
            "Search Tool: %s",
            query,
        )

        #
        # Retrieve conversational filters
        #

        filters = context.memory.variables.get(
            "filters",
            {},
        )

        #
        # Call your existing SearchService
        #

        result = self.search_service.search(
            query=query,
            limit=limit,
            filters=filters,
        )

        #
        # Store products for later tools
        #

        context.memory.products = result.get(
            "products",
            [],
        )

        return result