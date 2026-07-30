"""
Facet Models

Common DTOs used by the Facet Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FacetValue:
    """
    Single facet value.

    Example:
        White (18)
    """

    value: str
    count: int


@dataclass(slots=True)
class Facet:
    """
    Represents one facet.

    Example:

    {
        "name": "brand",
        "values": [...]
    }
    """

    name: str
    values: list[FacetValue] = field(default_factory=list)


@dataclass(slots=True)
class FacetResponse:
    """
    Final response returned by the FacetBuilder.
    """

    facets: dict[str, list[FacetValue]] = field(
        default_factory=dict
    )