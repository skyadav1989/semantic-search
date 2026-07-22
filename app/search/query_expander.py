from typing import Dict, List

class QueryExpander:
    """
    Expands a query using a synonym dictionary.
    """

    def __init__(self, synonyms: Dict[str, List[str]] | None = None):
        self.synonyms = synonyms or {
            "fan": ["ceiling fan", "wall fan", "pedestal fan"],
            "bulb": ["led bulb", "lamp"],
            "ac": ["air conditioner"]
        }

    def expand(self, query: str) -> dict:
        words = query.lower().split()
        expanded = set(words)

        for word in words:
            if word in self.synonyms:
                expanded.update(self.synonyms[word])

        return {
            "original_query": query,
            "expanded_terms": sorted(expanded),
            "expanded_query": " ".join(sorted(expanded))
        }
