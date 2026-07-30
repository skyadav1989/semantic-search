"""
Recommendation Engine Constants
"""

from __future__ import annotations

#
# Recommendation Types
#
SIMILAR = "similar"
ALTERNATIVE = "alternative"
COMPLEMENTARY = "complementary"
TRENDING = "trending"

#
# Defaults
#
DEFAULT_LIMIT = 10
MAX_LIMIT = 50
MIN_SIMILARITY_SCORE = 0.60

#
# Ranking Weights
#
SEMANTIC_WEIGHT = 0.55
BUSINESS_WEIGHT = 0.20
STOCK_WEIGHT = 0.15
PRICE_WEIGHT = 0.10

#
# Recommendation Strategies
#
STRATEGY_VECTOR = "vector"
STRATEGY_RULE = "rule"
STRATEGY_HYBRID = "hybrid"

#
# Business Rules
#
PRICE_VARIATION_PERCENT = 20
EXCLUDE_SOURCE_PRODUCT = True

#
# Supported Recommendation Modes
#
SUPPORTED_MODES = (
    SIMILAR,
    ALTERNATIVE,
    COMPLEMENTARY,
    TRENDING,
)