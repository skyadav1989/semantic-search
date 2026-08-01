"""
Context Manager

Maintains search context across multiple turns.

Responsibilities

- Update current search context
- Merge follow-up filters
- Store latest products
- Build effective query
"""

from __future__ import annotations

import copy
import logging

from .models import (
    ProductReference,
    SearchContext,
)

logger = logging.getLogger(__name__)


class ContextManager:
    """
    Maintains shopping context.
    """

    # ---------------------------------------------------------

    def update(
        self,
        *,
        context: SearchContext,
        query: str,
        normalized_query: str,
        filters: dict,
        attributes: dict,
        intent: str,
        products: list[ProductReference],
    ) -> SearchContext:
        """
        Replace current search context.
        """

        context.query = query

        context.normalized_query = normalized_query

        context.intent = intent

        context.filters = copy.deepcopy(filters)

        context.attributes = copy.deepcopy(attributes)

        context.products = list(products)

        return context

    # ---------------------------------------------------------

    def merge_filters(
        self,
        *,
        context: SearchContext,
        filters: dict,
    ) -> dict:
        """
        Merge new filters with previous filters.

        Example

        Existing:
            category=Fans

        New:
            color=White

        Result:
            category=Fans
            color=White
        """

        merged = copy.deepcopy(
            context.filters
        )

        merged.update(filters)

        return merged

    # ---------------------------------------------------------

    def merge_attributes(
        self,
        *,
        context: SearchContext,
        attributes: dict,
    ) -> dict:

        merged = copy.deepcopy(
            context.attributes
        )

        merged.update(attributes)

        return merged

    # ---------------------------------------------------------

    def latest_products(
        self,
        context: SearchContext,
    ) -> list[ProductReference]:

        return context.products

    # ---------------------------------------------------------

    def latest_query(
        self,
        context: SearchContext,
    ) -> str:

        return context.query

    # ---------------------------------------------------------

    def clear(
        self,
        context: SearchContext,
    ) -> None:

        context.query = ""

        context.normalized_query = ""

        context.intent = ""

        context.filters.clear()

        context.attributes.clear()

        context.products.clear()

    # ---------------------------------------------------------

    def has_context(
        self,
        context: SearchContext,
    ) -> bool:

        return bool(
            context.query
            or context.products
            or context.filters
        )

    # ---------------------------------------------------------

    def product_by_index(
        self,
        context: SearchContext,
        index: int,
    ) -> ProductReference | None:
        """
        Allows follow-up queries like

        Compare product 1

        Tell me more about product 2
        """

        if index < 1:
            return None

        if index > len(context.products):
            return None

        return context.products[
            index - 1
        ]

    # ---------------------------------------------------------

    def product_by_sku(
        self,
        context: SearchContext,
        sku: str,
    ) -> ProductReference | None:

        sku = sku.lower()

        for product in context.products:

            if product.sku.lower() == sku:
                return product

        return None

    # ---------------------------------------------------------

    def summary(
        self,
        context: SearchContext,
    ) -> dict:

        return {

            "query": context.query,

            "intent": context.intent,

            "filters": context.filters,

            "attributes": context.attributes,

            "products": len(
                context.products
            ),
        }