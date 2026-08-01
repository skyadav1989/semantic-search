"""
Agentic shopping planner for chat.

Phase 1 keeps planning deterministic: classify the turn, decide whether
search is useful, and ask for missing shopping context when the user only
provides constraints such as budget or color.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .models import SearchContext


@dataclass(slots=True)
class AgentPlan:
    """
    Planner output consumed by ChatService.
    """

    action: str
    objective: str
    effective_query: str
    requires_search: bool = True
    prompt_type: str = "search"
    clarification_question: str | None = None
    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "objective": self.objective,
            "effective_query": self.effective_query,
            "requires_search": self.requires_search,
            "prompt_type": self.prompt_type,
            "clarification_question": self.clarification_question,
            "signals": list(self.signals),
        }


class ShoppingAgentPlanner:
    """
    Lightweight shopping turn planner.
    """

    PRICE_ONLY_PATTERN = re.compile(
        r"^(under|below|less than|over|above|greater than|between)\s+\d+(\s*(and|to|-)\s*\d+)?$",
        re.I,
    )
    PRICE_SIGNAL_PATTERN = re.compile(
        r"\b(under|below|less than|over|above|greater than|between)\s+\d+",
        re.I,
    )
    COMPARE_PATTERN = re.compile(
        r"\b(compare|comparison|difference|differences|versus|vs\.?|better)\b",
        re.I,
    )
    DETAIL_PATTERN = re.compile(
        r"\b(tell me more|details?|specs?|specifications?|more about|explain)\b",
        re.I,
    )
    PRODUCT_REFERENCE_PATTERN = re.compile(
        r"\b(product|item|option)\s*#?\s*\d+\b|\b\d+(st|nd|rd|th)\b",
        re.I,
    )

    ATTRIBUTE_ONLY_WORDS = {
        "white",
        "black",
        "brown",
        "gold",
        "silver",
        "remote",
        "bldc",
        "smart",
        "wifi",
        "inverter",
        "silent",
        "energy",
        "star",
        "premium",
        "cheap",
        "cheaper",
        "best",
        "havells",
        "crompton",
        "orient",
        "usha",
        "bajaj",
    }

    CATEGORY_WORDS = {
        "fan",
        "fans",
        "ceiling fan",
        "light",
        "lights",
        "bulb",
        "bulbs",
        "washing machine",
        "refrigerator",
        "fridge",
        "cooler",
        "geyser",
        "heater",
        "appliance",
        "appliances",
    }

    def plan(
        self,
        *,
        query: str,
        context: SearchContext,
        previous_query: str | None = None,
    ) -> AgentPlan:
        cleaned = " ".join(query.strip().split())
        normalized = cleaned.lower()
        has_context = bool(previous_query or context.products or context.filters)
        signals = self._signals(normalized)

        if not cleaned:
            return AgentPlan(
                action="clarify",
                objective="Ask for a shopping request",
                effective_query=cleaned,
                requires_search=False,
                clarification_question="What would you like to shop for?",
                signals=["empty_query"],
            )

        if self.COMPARE_PATTERN.search(normalized):
            if len(context.products) >= 2:
                return AgentPlan(
                    action="compare",
                    objective="Compare products from the current result set",
                    effective_query=cleaned,
                    prompt_type="compare",
                    signals=signals + ["compare_request"],
                )
            return self._clarify(
                cleaned,
                "I can compare products once I know which items or category you want. What should I compare?",
                signals + ["compare_without_context"],
            )

        if self.DETAIL_PATTERN.search(normalized) and self.PRODUCT_REFERENCE_PATTERN.search(normalized):
            if context.products:
                return AgentPlan(
                    action="detail",
                    objective="Explain a referenced product from the current result set",
                    effective_query=cleaned,
                    prompt_type="explanation",
                    signals=signals + ["detail_request"],
                )
            return self._clarify(
                cleaned,
                "Which product should I explain? You can ask for a category first, then refer to product 1 or product 2.",
                signals + ["detail_without_context"],
            )

        if self._constraint_only(normalized) and not has_context:
            return self._clarify(
                cleaned,
                "What product category should I search within that constraint? For example: fans under 500, LED lights under 500, or kitchen items under 500.",
                signals + ["constraint_without_context"],
            )

        if self._constraint_only(normalized) and has_context:
            effective_query = f"{previous_query} {cleaned}" if previous_query else cleaned
            return AgentPlan(
                action="refine_search",
                objective="Apply the user's constraint to the current shopping context",
                effective_query=effective_query,
                prompt_type="followup",
                signals=signals + ["contextual_refinement"],
            )

        return AgentPlan(
            action="search",
            objective="Search products that match the user's shopping request",
            effective_query=cleaned,
            prompt_type="search",
            signals=signals or ["product_search"],
        )

    def _clarify(
        self,
        query: str,
        question: str,
        signals: list[str],
    ) -> AgentPlan:
        return AgentPlan(
            action="clarify",
            objective="Collect missing shopping context before searching",
            effective_query=query,
            requires_search=False,
            clarification_question=question,
            signals=signals,
        )

    def _signals(self, query: str) -> list[str]:
        signals = []

        if self.PRICE_SIGNAL_PATTERN.search(query):
            signals.append("price_constraint")

        if any(word in query for word in self.CATEGORY_WORDS):
            signals.append("category_signal")

        if self._attribute_only(query):
            signals.append("attribute_constraint")

        return signals

    def _constraint_only(self, query: str) -> bool:
        return bool(
            self.PRICE_ONLY_PATTERN.fullmatch(query)
            or self._attribute_only(query)
        )

    def _attribute_only(self, query: str) -> bool:
        words = set(re.findall(r"[a-z0-9]+", query))
        if not words:
            return False
        return words.issubset(self.ATTRIBUTE_ONLY_WORDS)
