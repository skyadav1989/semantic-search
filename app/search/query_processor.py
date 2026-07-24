"""
Query Processor

Pipeline

Raw Query
    ↓
Normalizer
    ↓
Intent Detection
    ↓
Attribute Extraction
"""

from __future__ import annotations

from .query_normalizer import QueryNormalizer
from .intent_detector import IntentDetector
from .attribute_extractor import AttributeExtractor


class QueryProcessor:

    def __init__(self, registry):

        self.norm = QueryNormalizer()

        self.intent = IntentDetector()

        self.attrs = AttributeExtractor(
            registry
        )

    # ---------------------------------------------------------

    def process(
        self,
        query: str,
    ) -> dict:

        normalized = self.norm.normalize(
            query
        )

        attributes = self.attrs.extract(
            normalized
        )

        intent = self.intent.detect(
            normalized
        )

        return {

            "normalized_query": normalized,

            "intent": intent,

            "attributes": attributes,

        }