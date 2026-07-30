"""
Recommendation Engine Exceptions
"""

from __future__ import annotations


class RecommendationError(Exception):
    """
    Base exception for recommendation engine.
    """

    default_message = "Recommendation engine error."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class ProductNotFoundError(RecommendationError):
    """
    Raised when the source SKU is not found.
    """

    default_message = "Source product not found."


class InvalidRecommendationTypeError(RecommendationError):
    """
    Raised when recommendation type is invalid.
    """

    default_message = "Unsupported recommendation type."


class CandidateNotFoundError(RecommendationError):
    """
    Raised when no recommendation candidates exist.
    """

    default_message = "No recommendation candidates found."


class RecommendationConfigurationError(RecommendationError):
    """
    Raised when engine configuration is invalid.
    """

    default_message = "Recommendation engine configuration error."


class SimilarityCalculationError(RecommendationError):
    """
    Raised when similarity calculation fails.
    """

    default_message = "Unable to calculate similarity score."


class BusinessRuleError(RecommendationError):
    """
    Raised when business rule evaluation fails.
    """

    default_message = "Business rule evaluation failed."


class RecommendationLimitError(RecommendationError):
    """
    Raised when requested recommendation limit is invalid.
    """

    default_message = "Invalid recommendation limit."