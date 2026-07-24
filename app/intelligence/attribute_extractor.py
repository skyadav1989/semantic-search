"""
Generic Product Attribute Extractor

Reads attribute definitions from KnowledgeRegistry
instead of hardcoded dictionaries.

Works across all product categories.
"""

from __future__ import annotations

import re


class AttributeExtractor:

    def __init__(self, registry):

        self.registry = registry

        #
        # Build alias -> canonical lookup
        #
        self.key_mapping = {}

        mapping = registry.attribute_mapping.get(
            "canonical_attributes",
            {}
        )

        for canonical, aliases in mapping.items():

            for alias in aliases:

                self.key_mapping[
                    alias.lower().strip()
                ] = canonical

        #
        # Value mappings
        #
        self.value_mapping = registry.value_mapping

    # ---------------------------------------------------------

    def extract(self, raw: dict) -> dict:

        attributes = {}

        #
        # Technical Specifications
        #

        for key, value in raw.get(
            "technical_specifications",
            {},
        ).items():

            canonical = self.normalize_key(key)

            if not canonical:
                continue

            attributes[canonical] = self.normalize_value(
                canonical,
                value,
            )

        #
        # Variations
        #

        for variation in raw.get(
            "variations",
            [],
        ):

            key = variation.get("name", "")

            options = variation.get("options", [])

            if not options:
                continue

            canonical = self.normalize_key(key)

            if not canonical:
                continue

            attributes.setdefault(
                canonical,
                self.normalize_value(
                    canonical,
                    options[0],
                ),
            )

        #
        # Subtitle
        #

        subtitle = raw.get("subtitle", "")

        if "size" not in attributes:

            m = re.search(
                r"(\d+)\s*mm",
                subtitle,
                re.I,
            )

            if m:

                attributes["size"] = int(
                    m.group(1)
                )

        if "color" not in attributes:

            m = re.search(
                r"\((.*?)\)",
                subtitle,
            )

            if m:

                attributes["color"] = self.normalize_value(
                    "color",
                    m.group(1),
                )

        return attributes

    # ---------------------------------------------------------

    def normalize_key(self, key):

        return self.key_mapping.get(
            key.lower().strip()
        )

    # ---------------------------------------------------------

    def normalize_value(
        self,
        key,
        value,
    ):

        if value is None:
            return None

        value = str(value).strip()

        #
        # Color normalization
        #

        if key == "color":

            return self.normalize_from_yaml(
                "color",
                value,
            )

        #
        # Boolean normalization
        #

        if key in (
            "dimmable",
            "remote",
            "wifi",
            "bluetooth",
        ):

            return self.normalize_boolean(
                value
            )

        #
        # Numeric normalization
        #

        m = re.search(
            r"[\d.]+",
            value.replace(",", ""),
        )

        if m:

            number = float(
                m.group()
            )

            if number.is_integer():

                return int(number)

            return number

        return value

    # ---------------------------------------------------------

    def normalize_boolean(
        self,
        value,
    ):

        value = value.lower()

        false_values = (
            self.value_mapping
            .get("boolean", {})
            .get(False, [])
        )

        false_values += (
            self.value_mapping
            .get("boolean", {})
            .get("false", [])
        )

        return value not in [
            str(v).lower()
            for v in false_values
        ]

    # ---------------------------------------------------------

    def normalize_from_yaml(
        self,
        section,
        value,
    ):

        value = value.lower().strip()

        section_map = self.value_mapping.get(
            section,
            {},
        )

        for canonical, aliases in section_map.items():

            aliases = [
                str(a).lower()
                for a in aliases
            ]

            if value in aliases:

                return canonical

        return value