"""
FAQ Formatter

Formats knowledge documents into LLM-ready context.

Responsibilities

- Format retrieved FAQ documents
- Build context string
- Build source list
- Limit context size
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class FAQFormatter:
    """
    Formats FAQ documents.
    """

    def __init__(
        self,
        *,
        max_documents: int = 5,
        max_content_length: int = 800,
    ):
        self.max_documents = max_documents
        self.max_content_length = max_content_length

    # ---------------------------------------------------------

    def format(
        self,
        documents: list[dict],
    ) -> str:
        """
        Build LLM context.
        """

        if not documents:
            return ""

        lines = []

        for index, document in enumerate(
            documents[: self.max_documents],
            start=1,
        ):

            title = document.get("title", "").strip()

            content = document.get("content", "").strip()

            source = document.get("source", "").strip()

            category = document.get("category", "").strip()

            score = float(document.get("score", 0))

            if len(content) > self.max_content_length:
                content = (
                    content[: self.max_content_length].rstrip()
                    + "..."
                )

            lines.append(f"Document {index}")

            if title:
                lines.append(f"Title: {title}")

            if category:
                lines.append(f"Category: {category}")

            if source:
                lines.append(f"Source: {source}")

            lines.append(f"Score: {score:.3f}")

            lines.append("Content:")

            lines.append(content)

            lines.append("")

        return "\n".join(lines)

    # ---------------------------------------------------------

    def sources(
        self,
        documents: list[dict],
    ) -> list[str]:
        """
        Return unique source list.
        """

        sources = []

        seen = set()

        for document in documents:

            source = document.get("source")

            if not source:
                continue

            if source in seen:
                continue

            seen.add(source)

            sources.append(source)

        return sources

    # ---------------------------------------------------------

    def titles(
        self,
        documents: list[dict],
    ) -> list[str]:

        return [

            document["title"]

            for document in documents

            if document.get("title")

        ]

    # ---------------------------------------------------------

    def metadata(
        self,
        documents: list[dict],
    ) -> dict:
        """
        Build formatter metadata.
        """

        if not documents:

            return {
                "documents": 0,
                "sources": [],
            }

        return {

            "documents": len(documents),

            "sources": self.sources(documents),

            "average_score": round(

                sum(
                    float(
                        d.get("score", 0)
                    )
                    for d in documents
                )
                / len(documents),

                3,

            ),
        }

    # ---------------------------------------------------------

    def explain(
        self,
        documents: list[dict],
    ) -> dict:
        """
        Debug formatter.
        """

        return {

            "titles": self.titles(documents),

            "sources": self.sources(documents),

            "metadata": self.metadata(documents),

            "context": self.format(documents),

        }