"""
Query Attribute Extractor

Extracts structured filters from a search query.

Uses the KnowledgeRegistry instead of hardcoded values.

Examples

"white ceiling fan below 5000"

↓

{
    "color":"white",
    "category":"Ceiling Fans",
    "max_price":5000
}
"""

from __future__ import annotations

import re


class AttributeExtractor:

    def __init__(self, registry):

        self.registry = registry

        self.value_mapping = registry.value_mapping

        self.categories = registry.categories

        self.brands = [
            b.lower()
            for b in registry.brands.get("brands", [])
        ]

    # ------------------------------------------------------------

    def extract(
        self,
        query: str,
    ) -> dict:

        query = query.lower()

        attributes = {}

        #
        # Price
        #

        m = re.search(
            r"(?:under|below|less than)\s*(\d+)",
            query,
        )

        if m:

            attributes["max_price"] = int(
                m.group(1)
            )

        m = re.search(
            r"(?:above|over|greater than)\s*(\d+)",
            query,
        )

        if m:

            attributes["min_price"] = int(
                m.group(1)
            )

        #
        # Brand
        #

        for brand in self.brands:

            if brand in query:

                attributes["brand"] = brand.title()

                break

        #
        # Category / Subcategory
        #

        categories = self.categories.get(
            "categories",
            {},
        )

        for parent, children in categories.items():

            parent_lower = parent.lower()

            if parent_lower in query:

                attributes["category"] = parent

            for child in children:

                child_lower = child.lower()

                #
                # Exact match
                #
                if child_lower in query:

                    attributes["category"] = parent
                    attributes["subcategory"] = child
                    break

                #
                # Singular/plural match
                #
                child_tokens = child_lower.replace("-", " ").split()

                if all(
                    token.rstrip("s") in query
                    for token in child_tokens
                ):

                    attributes["category"] = parent
                    attributes["subcategory"] = child
                    break

        #
        # Generic value mappings
        #

        for section, mapping in self.value_mapping.items():

            if not isinstance(mapping, dict):
                continue

            for canonical, aliases in mapping.items():

                aliases = [
                    str(x).lower()
                    for x in aliases
                ]

                if any(
                    alias in query
                    for alias in aliases
                ):

                    attributes[section] = canonical

                    break

        #
        # Size
        #

        m = re.search(
            r"(\d+)\s*mm",
            query,
        )

        if m:

            attributes["size"] = int(
                m.group(1)
            )

        #
        # Power
        #

        m = re.search(
            r"(\d+)\s*w(?:att)?",
            query,
        )

        if m:

            attributes["power"] = int(
                m.group(1)
            )

        #
        # Capacity
        #

        m = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:l|litre|liter)",
            query,
        )

        if m:

            attributes["capacity"] = float(
                m.group(1)
            )

        return attributes