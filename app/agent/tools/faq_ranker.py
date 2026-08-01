"""
FAQ Ranker

Ranks retrieved knowledge documents.

Responsibilities

- Remove duplicates
- Sort by relevance
- Filter low-confidence documents
- Return top documents
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class FAQRanker:
    """
    Knowledge ranking component.
    """

    def __init__(
        self,
        *,
        min_score: float = 0.30,
    ):
        self.min_score = min_score

    # ---------------------------------------------------------

    def rank(
        self,
        documents: list[dict],
        *,
        limit: int = 5,
    ) -> list[dict]:
        """
        Rank FAQ documents.
        """

        if not documents:
            return []

        #
        # Remove duplicates
        #

        documents = self._remove_duplicates(
            documents,
        )

        #
        # Remove low score
        #

        documents = [

            doc

            for doc in documents

            if float(
                doc.get("score", 0)
            ) >= self.min_score

        ]

        #
        # Highest score first
        #

        documents.sort(

            key=lambda d: float(
                d.get("score", 0)
            ),

            reverse=True,

        )

        logger.info(

            "Ranked %d FAQ documents",

            len(documents),

        )

        return documents[:limit]

    # ---------------------------------------------------------

    def _remove_duplicates(
        self,
        documents: list[dict],
    ) -> list[dict]:

        unique = []

        seen = set()

        for document in documents:

            key = (

                document.get("id")

                or document.get("title")

                or document.get("content")

            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(document)

        return unique

    # ---------------------------------------------------------

    def best(
        self,
        documents: list[dict],
    ) -> dict | None:
        """
        Return highest ranked document.
        """

        ranked = self.rank(
            documents,
            limit=1,
        )

        if not ranked:
            return None

        return ranked[0]

    # ---------------------------------------------------------

    def explain(
        self,
        documents: list[dict],
    ) -> list[dict]:
        """
        Explain ranking for debugging.
        """

        ranked = self.rank(
            documents,
            limit=len(documents),
        )

        return [

            {

                "title": doc.get("title"),

                "score": doc.get("score"),

                "source": doc.get("source"),

            }

            for doc in ranked

        ]