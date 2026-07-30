"""
Recommendation Engine Enums
"""

from __future__ import annotations

from enum import Enum


class RecommendationType(str, Enum):
    """
    Types of recommendations supported by the engine.
    """

    SIMILAR = "similar"
    ALTERNATIVE = "alternative"
    COMPLEMENTARY = "complementary"
    TRENDING = "trending"


class RecommendationStrategy(str, Enum):
    """
    Recommendation generation strategy.
    """

    VECTOR = "vector"
    RULE = "rule"
    HYBRID = "hybrid"


class SortOrder(str, Enum):
    """
    Recommendation sorting.
    """

    SCORE = "score"
    PRICE_LOW_TO_HIGH = "price_low_to_high"
    PRICE_HIGH_TO_LOW = "price_high_to_low"
    NEWEST = "newest"


class ScoreComponent(str, Enum):
    """
    Individual scoring components.
    """

    SEMANTIC = "semantic"
    BUSINESS = "business"
    STOCK = "stock"
    PRICE = "price"