"""
Recommendation Engine Models
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RecommendationRequest:
    """
    Recommendation request.
    """

    sku: str
    recommendation_type: str = "similar"
    limit: int = 10
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RecommendationScore:
    """
    Score breakdown.
    """

    semantic: float = 0.0
    business: float = 0.0
    stock: float = 0.0
    price: float = 0.0
    final: float = 0.0


@dataclass(slots=True)
class RecommendationItem:
    """
    Recommended product.
    """

    sku: str
    score: RecommendationScore
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RecommendationResponse:
    """
    Recommendation response.
    """

    source_sku: str
    recommendation_type: str
    total: int
    recommendations: list[RecommendationItem] = field(default_factory=list)


@dataclass(slots=True)
class ProductVector:
    """
    Product embedding information.
    """

    sku: str
    vector: list[float]
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CandidateProduct:
    """
    Internal candidate used during ranking.
    """

    sku: str
    semantic_score: float
    payload: dict[str, Any] = field(default_factory=dict)