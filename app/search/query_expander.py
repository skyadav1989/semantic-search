"""
Query Expander

Expands search queries using the Knowledge Registry.

Example

Query:
    ceiling fan

Expanded:
    ceiling fan electric fan

Synonyms come from:

knowledge/v1/synonyms.yaml
"""

from __future__ import annotations


class QueryExpander:

    def __init__(self, registry):

        self.registry = registry

        self.synonyms = registry.synonyms.get(
            "synonyms",
            {}
        )

    # ---------------------------------------------------------

    def expand(
        self,
        query: str,
    ) -> dict:

        words = query.lower().split()

        expanded = []

        seen = set()

        for word in words:

            #
            # Original word
            #

            if word not in seen:
                expanded.append(word)
                seen.add(word)

            #
            # Synonyms
            #

            values = self.synonyms.get(
                word,
                []
            )

            for synonym in values:

                synonym = synonym.lower()

                if synonym not in seen:

                    expanded.append(
                        synonym
                    )

                    seen.add(
                        synonym
                    )

        return {

            "expanded_query": " ".join(expanded),

            "expanded_terms": expanded,

        }