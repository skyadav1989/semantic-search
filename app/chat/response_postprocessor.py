"""
Response Post Processor

Responsible for cleaning and enriching the final
LLM response before returning it to the client.

Responsibilities

- Trim whitespace
- Remove duplicate products
- Limit product count
- Generate follow-up questions
- Normalize citations
- Build final response
"""

from __future__ import annotations

from typing import Any


class ResponsePostProcessor:
    """
    Post-process chat responses.
    """

    DEFAULT_FOLLOWUPS = [
        "Show cheaper options",
        "Show premium options",
        "Only in-stock products",
        "Compare similar products",
    ]

    # ---------------------------------------------------------

    def process(
        self,
        *,
        answer: str,
        products: list[dict],
        citations: list[dict] | None = None,
        metadata: dict | None = None,
        limit: int = 10,
    ) -> dict:
        """
        Build final API response.
        """

        answer = self._clean_answer(answer)

        products = self._deduplicate_products(products)

        products = products[:limit]

        citations = self._normalize_citations(
            citations,
            products,
        )

        return {
            "answer": answer,
            "products": products,
            "citations": citations,
            "follow_up_questions": self._followups(products),
            "metadata": metadata or {},
        }

    # ---------------------------------------------------------

    def _clean_answer(
        self,
        answer: str,
    ) -> str:

        if not answer:
            return ""

        answer = answer.strip()

        while "\n\n\n" in answer:
            answer = answer.replace(
                "\n\n\n",
                "\n\n",
            )

        return answer

    # ---------------------------------------------------------

    def _deduplicate_products(
        self,
        products: list[dict],
    ) -> list[dict]:

        unique = []

        seen = set()

        for product in products:

            sku = product.get("sku")

            if not sku:
                continue

            if sku in seen:
                continue

            seen.add(sku)

            unique.append(product)

        return unique

    # ---------------------------------------------------------

    def _normalize_citations(
        self,
        citations: list[dict] | None,
        products: list[dict],
    ) -> list[dict]:

        if citations:
            return citations

        result = []

        for product in products:

            result.append(
                {
                    "sku": product.get("sku"),
                    "title": product.get("title"),
                    "url": product.get("url"),
                }
            )

        return result

    # ---------------------------------------------------------

    def _followups(
        self,
        products: list[dict],
    ) -> list[str]:

        if not products:

            return [
                "Try another search",
            ]

        first = products[0]

        category = first.get("category")

        if category:

            return [
                f"Show more {category}",
                "Show cheaper options",
                "Only in-stock products",
                "Sort by price",
            ]

        return list(self.DEFAULT_FOLLOWUPS)

    # ---------------------------------------------------------

    def empty(
        self,
        query: str,
    ) -> dict:
        """
        Empty search response.
        """

        return {
            "answer": (
                f"I couldn't find any products matching '{query}'. "
                "Try another search."
            ),
            "products": [],
            "citations": [],
            "follow_up_questions": [
                "Try another search",
            ],
            "metadata": {},
        }

    # ---------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> dict:
        """
        Error response.
        """

        return {
            "answer": message,
            "products": [],
            "citations": [],
            "follow_up_questions": [],
            "metadata": {},
        }