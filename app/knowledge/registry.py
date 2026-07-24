"""
Knowledge Registry

Loads all knowledge once and exposes it
to the rest of the application.

Everything should access knowledge through
this registry instead of reading YAML files
directly.
"""

from __future__ import annotations

from app.knowledge.loader import KnowledgeLoader


class KnowledgeRegistry:
    """
    Central Knowledge Registry.
    """

    def __init__(self, directory):

        self.loader = KnowledgeLoader(directory)

        self.knowledge = self.loader.load()

        #
        # Core
        #
        self.manifest = self.get("manifest", {})
        self.taxonomy = self.get("taxonomy", {})
        self.synonyms = self.get("synonyms", {})
        self.stopwords = self.get("stopwords", {})

        #
        # Intelligence
        #
        self.product_types = self.get("product_types", {})
        self.use_cases = self.get("use_cases", {})
        self.feature_benefits = self.get("feature_benefits", {})

        #
        # Generic Metadata
        #
        self.attribute_mapping = self.get(
            "attribute_mapping",
            {},
        )

        self.value_mapping = self.get(
            "value_mapping",
            {},
        )

        self.categories = self.get(
            "categories",
            {},
        )

        self.brands = self.get(
            "brands",
            {},
        )

        self.units = self.get(
            "units",
            {},
        )

        self.feature_groups = self.get(
            "feature_groups",
            {},
        )

        #
        # Search
        #
        self.query_patterns = self.get(
            "query_patterns",
            {},
        )

        self.ranking_rules = self.get(
            "ranking_rules",
            {},
        )

    # ---------------------------------------------------------

    def get(self, key, default=None):
        return self.knowledge.documents.get(
            key,
            default,
        )

    # ---------------------------------------------------------

    def has(self, key):
        return key in self.knowledge.documents

    # ---------------------------------------------------------

    def keys(self):
        return self.knowledge.documents.keys()

    # ---------------------------------------------------------

    def reload(self):

        self.knowledge = self.loader.load()

    # ---------------------------------------------------------

    def __contains__(self, item):
        return item in self.knowledge.documents

    # ---------------------------------------------------------

    def __getitem__(self, item):
        return self.knowledge.documents[item]