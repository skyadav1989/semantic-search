"""
Knowledge Search Service

Searches the knowledge repository.

Current Backend

    KnowledgeRegistry

Future Backends

    Qdrant
    Elasticsearch
    Markdown
    PDF
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class KnowledgeSearchService:
    """
    Searches the knowledge repository.
    """

    def __init__(
        self,
        *,
        registry,
    ):
        self.registry = registry

    # ---------------------------------------------------------

    def search(
        self,
        *,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Search knowledge.
        """

        query = query.lower().strip()

        if not query:
            return []

        documents = []

        #
        # Search every loaded knowledge section
        #

        print("=" * 80)
        print(type(self.registry))
        print(self.registry.keys())
        print("=" * 80)


        
        for section_name in self.registry.keys():

            section_data = self.registry.get(
                section_name,
                {},
            )

            documents.extend(
                self._search_section(
                    section_name,
                    section_data,
                    query,
                )
            )
            if section_name == "technical_specs":
                print("=" * 80)
                print("TECHNICAL SPECS")
                print(type(section_data))
                print(section_data)
                print("=" * 80)

        #
        # Highest score first
        #

        documents.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return documents[:limit]

    # ---------------------------------------------------------

    def _search_section(
        self,
        section_name: str,
        data,
        query: str,
    ) -> list[dict]:

        results = []

        #
        # Dictionary
        #

        if isinstance(data, dict):

            for key, value in data.items():

                score = self._score(
                    query,
                    key,
                    value,
                )

                print(
                    section_name,
                    key,
                    score,
                )

                if score <= 0:
                    continue

                results.append(
                    {
                        "id": f"{section_name}:{key}",
                        "title": str(key),
                        "content": self._to_text(value),
                        "category": section_name,
                        "source": section_name,
                        "score": score,
                    }
                )

        #
        # List
        #

        elif isinstance(data, list):

            for index, item in enumerate(data):

                score = self._score(
                    query,
                    "",
                    item,
                )

                if score <= 0:
                    continue

                results.append(
                    {
                        "id": f"{section_name}:{index}",
                        "title": section_name,
                        "content": self._to_text(item),
                        "category": section_name,
                        "source": section_name,
                        "score": score,
                    }
                )

        return results

    # ---------------------------------------------------------

    def _score(
        self,
        query: str,
        title,
        content,
    ) -> float:

        title = str(title).lower()

        content = self._to_text(content).lower()

        score = 0.0

        STOPWORDS = {
            "what","is","are","the","a","an",
            "how","why","does","do","can",
            "i","of","to","for",
        }

        tokens = [
            t
            for t in query.split()
            if t not in STOPWORDS
        ]

        for token in tokens:

            #
            # Exact title
            #
            if token == title:
                score += 20

            #
            # Partial title
            #
            elif token in title:
                score += 10

            #
            # Content
            #
            if token in content:
                score += 5

        return score

    # ---------------------------------------------------------

    def _to_text(
        self,
        value,
    ) -> str:

        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if isinstance(value, list):
            return " ".join(
                self._to_text(v)
                for v in value
            )

        if isinstance(value, dict):
            return " ".join(
                f"{k} {self._to_text(v)}"
                for k, v in value.items()
            )

        return str(value)