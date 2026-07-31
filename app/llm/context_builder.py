"""
LLM Context Builder

Converts semantic search results into a compact context
that is passed to the LLM.

This is the ONLY place responsible for formatting product
information for prompts.
"""

from __future__ import annotations

import logging

from .constants import MAX_PRODUCTS_IN_CONTEXT
from .models import ProductContext

logger = logging.getLogger(__name__)


class ContextBuilder:
    """
    Build LLM context from search results.
    """

    def build(
        self,
        results: list[dict],
        limit: int = MAX_PRODUCTS_IN_CONTEXT,
    ) -> tuple[list[ProductContext], str]:
        """
        Returns

        ProductContext list
        +
        Prompt context string
        """

        contexts: list[ProductContext] = []

        blocks: list[str] = []

        for index, result in enumerate(results[:limit], start=1):

            payload = result.get("payload", {})

            product = ProductContext(

                sku=payload.get("sku", ""),

                title=payload.get("title", ""),

                category=payload.get("category", ""),

                subcategory=payload.get("subcategory", ""),

                brand=payload.get("brand", ""),

                price=payload.get("price", 0),

                mrp=payload.get("mrp", 0),

                stock_status=payload.get(
                    "stock_status",
                    "",
                ),

                url=payload.get("url", ""),

                image=payload.get("image", ""),

                attributes=payload.get(
                    "attributes",
                    {},
                ),

                benefits=payload.get(
                    "benefits",
                    [],
                ),

                use_cases=payload.get(
                    "use_cases",
                    [],
                ),

                technical_specs=payload.get(
                    "technical_specs",
                    {},
                ),
            )

            contexts.append(product)

            blocks.append(
                self._format_product(
                    index,
                    product,
                )
            )

        logger.info(
            "Prepared %d products for LLM context",
            len(contexts),
        )

        return contexts, "\n\n".join(blocks)

    # -----------------------------------------------------

    def _format_product(
        self,
        index: int,
        product: ProductContext,
    ) -> str:
        """
        Convert one product into prompt context.
        """

        lines = [

            f"Product {index}",

            f"SKU: {product.sku}",

            f"Title: {product.title}",

            f"Category: {product.category}",

            f"Subcategory: {product.subcategory}",

            f"Brand: {product.brand}",

            f"Price: ₹{product.price}",

            f"MRP: ₹{product.mrp}",

            f"Availability: {product.stock_status}",
        ]

        #
        # Attributes
        #
        if product.attributes:

            lines.append("Attributes:")

            for key, value in product.attributes.items():

                lines.append(
                    f"- {key}: {value}"
                )

        #
        # Benefits
        #
        if product.benefits:

            lines.append("Benefits:")

            for benefit in product.benefits:

                lines.append(
                    f"- {benefit}"
                )

        #
        # Use Cases
        #
        if product.use_cases:

            lines.append("Use Cases:")

            for use_case in product.use_cases:

                lines.append(
                    f"- {use_case}"
                )

        #
        # Technical Specs
        #
        if product.technical_specs:

            lines.append("Technical Specifications:")

            for key, value in product.technical_specs.items():

                lines.append(
                    f"- {key}: {value}"
                )

        return "\n".join(lines)