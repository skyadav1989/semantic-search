"""
Facet Utilities

Reusable helper functions for facet generation.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .models import FacetValue


def normalize_value(value: Any) -> str | None:
    """
    Normalize facet values.

    Examples
    --------
    " White " -> "White"
    "" -> None
    None -> None
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    return value


def increment(counter: Counter, value: Any) -> None:
    """
    Increment a Counter safely.
    """

    value = normalize_value(value)

    if value is None:
        return

    counter[value] += 1


def counter_to_facet(counter: Counter, limit: int = 10) -> list[FacetValue]:
    """
    Convert Counter into FacetValue list.

    Highest count first.
    """

    values: list[FacetValue] = []

    for value, count in counter.most_common(limit):
        values.append(
            FacetValue(
                value=value,
                count=count,
            )
        )

    return values


def sort_numeric_strings(values: list[str]) -> list[str]:
    """
    Sort strings like

    300 mm
    450 mm
    600 mm

    numerically.
    """

    def key(v: str):

        number = ""

        for ch in v:
            if ch.isdigit() or ch == ".":
                number += ch

        try:
            return float(number)
        except ValueError:
            return float("inf")

    return sorted(values, key=key)


def remove_empty_facets(
    facets: dict[str, list[FacetValue]],
) -> dict[str, list[FacetValue]]:
    """
    Remove empty facet groups.
    """

    return {
        key: values
        for key, values in facets.items()
        if values
    }