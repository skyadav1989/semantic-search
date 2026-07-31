"""
LLM Response Formatter

Formats LLM output into a consistent API response.
"""

from __future__ import annotations

from .models import (
    ChatResponse,
    ProductContext,
)


class ResponseFormatter:
    """
    Formats responses returned by the LLM.
    """

    def format(
        self,
        response: ChatResponse,
    ) -> dict:

        return {
            "query": response.query,

            "answer": response.answer,

            "products": [
                self._product(product)
                for product in response.products
            ],

            "citations": response.citations,

            "metadata": response.metadata,
        }

    # ---------------------------------------------------------

    def _product(
        self,
        product: ProductContext,
    ) -> dict:

        return {

            "sku": product.sku,

            "title": product.title,

            "category": product.category,

            "subcategory": product.subcategory,

            "brand": product.brand,

            "price": product.price,

            "mrp": product.mrp,

            "stock_status": product.stock_status,

            "url": product.url,

            "image": product.image,

            "attributes": product.attributes,
        }

    # ---------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> dict:

        return {
            "success": False,
            "answer": "",

            "error": message,

            "products": [],

            "citations": [],

            "metadata": {},
        }

    # ---------------------------------------------------------

    def success(
        self,
        response: ChatResponse,
    ) -> dict:

        data = self.format(response)

        data["success"] = True

        return data