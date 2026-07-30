"""
Recommendation Engine Utilities
"""

from __future__ import annotations

import math
from typing import Iterable

from .models import CandidateProduct, RecommendationScore


# ---------------------------------------------------------
# Numeric Helpers
# ---------------------------------------------------------


def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 1.0,
) -> float:
    """
    Clamp value between min and max.
    """

    return max(minimum, min(value, maximum))


def safe_divide(
    numerator: float,
    denominator: float,
    default: float = 0.0,
) -> float:
    """
    Safe division.
    """

    if denominator == 0:
        return default

    return numerator / denominator


# ---------------------------------------------------------
# Similarity
# ---------------------------------------------------------


def cosine_similarity(
    vector1: list[float],
    vector2: list[float],
) -> float:
    """
    Compute cosine similarity.
    """

    if not vector1 or not vector2:
        return 0.0

    if len(vector1) != len(vector2):
        return 0.0

    dot = sum(a * b for a, b in zip(vector1, vector2))

    norm1 = math.sqrt(sum(v * v for v in vector1))
    norm2 = math.sqrt(sum(v * v for v in vector2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


def normalize_score(
    score: float,
) -> float:
    """
    Normalize score to 0-1.
    """

    return clamp(score)


def price_similarity(
    source_price: float,
    candidate_price: float,
) -> float:
    """
    Calculate price similarity.
    """

    if source_price <= 0 or candidate_price <= 0:
        return 0.0

    difference = abs(source_price - candidate_price)

    return clamp(
        1 - (difference / max(source_price, candidate_price))
    )


# ---------------------------------------------------------
# Candidate Helpers
# ---------------------------------------------------------


def deduplicate_candidates(
    candidates: Iterable[CandidateProduct],
) -> list[CandidateProduct]:
    """
    Remove duplicate SKUs.
    """

    seen = set()

    unique = []

    for candidate in candidates:

        if candidate.sku in seen:
            continue

        seen.add(candidate.sku)

        unique.append(candidate)

    return unique


def sort_candidates(
    candidates: list[CandidateProduct],
) -> list[CandidateProduct]:
    """
    Sort by semantic score.
    """

    return sorted(
        candidates,
        key=lambda item: item.semantic_score,
        reverse=True,
    )


# ---------------------------------------------------------
# Recommendation Score
# ---------------------------------------------------------


def merge_scores(
    semantic: float,
    business: float,
    stock: float,
    price: float,
    semantic_weight: float,
    business_weight: float,
    stock_weight: float,
    price_weight: float,
) -> RecommendationScore:
    """
    Build RecommendationScore object.
    """

    final = (
        semantic * semantic_weight
        + business * business_weight
        + stock * stock_weight
        + price * price_weight
    )

    return RecommendationScore(
        semantic=semantic,
        business=business,
        stock=stock,
        price=price,
        final=round(final, 6),
    ) 