"""
Citation Builder

Builds citations from retrieved products.
"""

from __future__ import annotations

from .models import (
    Citation,
    ProductContext,
)


class CitationBuilder:
    """
    Creates citations for LLM responses.
    """

    def build(
        self,
        products: list[ProductContext],
    ) -> list[Citation]:

        citations: list[Citation] = []

        for product in products:

            citations.append(
                Citation(
                    sku=product.sku,
                    title=product.title,
                    url=product.url,
                )
            )

        return citations

    # ---------------------------------------------------------

    def markdown(
        self,
        citations: list[Citation],
    ) -> str:
        """
        Markdown citations.
        """

        if not citations:
            return ""

        lines = []

        lines.append("### Sources")

        for citation in citations:

            lines.append(
                f"- **{citation.title}** ({citation.sku})"
            )

            if citation.url:

                lines.append(
                    f"  {citation.url}"
                )

        return "\n".join(lines)

    # ---------------------------------------------------------

    def json(
        self,
        citations: list[Citation],
    ) -> list[dict]:

        return [
            {
                "sku": citation.sku,
                "title": citation.title,
                "url": citation.url,
            }
            for citation in citations
        ]

    # ---------------------------------------------------------

    def lookup(
        self,
        sku: str,
        citations: list[Citation],
    ) -> Citation | None:

        for citation in citations:

            if citation.sku == sku:
                return citation

        return None