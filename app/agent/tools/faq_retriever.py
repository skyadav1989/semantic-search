"""
FAQ Retriever

Responsible for retrieving relevant knowledge
documents for FAQ queries.

The retriever is storage-independent.

Supported future sources

- YAML
- JSON
- Markdown
- PDF
- Qdrant
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class FAQRetriever:
    """
    Retrieves knowledge documents.
    """

    def __init__(
        self,
        *,
        knowledge_search,
    ):
        self.knowledge_search = knowledge_search

    # ---------------------------------------------------------

    def retrieve(
        self,
        *,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Retrieve FAQ documents.
        """

        logger.info(
            "Searching knowledge: %s",
            query,
        )

        documents = self.knowledge_search.search(
            query=query,
            limit=limit,
        )

        logger.info(
            "Retrieved %d document(s)",
            len(documents),
        )

        return [
            self._normalize(document)
            for document in documents
        ]

    # ---------------------------------------------------------

    def _normalize(
        self,
        document: dict,
    ) -> dict:
        """
        Normalize document.
        """

        return {

            "id": document.get("id"),

            "title": document.get("title", ""),

            "content": document.get("content", ""),

            "source": document.get("source", ""),

            "category": document.get("category"),

            "score": float(
                document.get("score", 0.0)
            ),
        }