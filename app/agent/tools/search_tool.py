"""
Search Tool

Delegates product search to the SearchService.
"""

from __future__ import annotations

import logging

from app.agent.models import ExecutionContext

logger = logging.getLogger(__name__)


class SearchTool:
    """
    Product search tool.
    """

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
        """
        Execute product search.
        """

        logger.info(
            "Search Tool: %s",
            query,
        )

        #
        # Conversation filters
        #

        filters = context.memory.variables.get(
            "filters",
            {},
        )

        #
        # Existing SearchService
        #

        try:
            result = self.search_service.search(
                query=query,
                limit=limit,
                filters=filters,
            )
        except TypeError:
            #
            # Existing SearchService may not yet support filters.
            #
            result = self.search_service.search(
                query=query,
                limit=limit,
            )

        #
        # Save products for later planner steps
        #

        context.memory.products = result.get(
            "products",
            [],
        )

        return result