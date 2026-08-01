"""
State Manager

Maintains conversation state for the Shopping Agent.

Responsibilities

- Update conversation history
- Merge filters
- Store search results
- Store selected products
- Store comparison products
- Update planner state
- Store preferences

No retrieval or LLM logic belongs here.
"""

from __future__ import annotations

import logging
from typing import Any

from .memory import (
    ConversationMemory,
    ConversationTurn,
    PlannerState,
    ProductReference,
)

logger = logging.getLogger(__name__)


class StateManager:
    """
    Updates ConversationMemory.
    """

    # ---------------------------------------------------------

    def add_user_message(
        self,
        memory: ConversationMemory,
        message: str,
    ) -> None:

        memory.history.append(

            ConversationTurn(
                role="user",
                message=message,
            )

        )

        memory.touch()

    # ---------------------------------------------------------

    def add_assistant_message(
        self,
        memory: ConversationMemory,
        message: str,
    ) -> None:

        memory.history.append(

            ConversationTurn(
                role="assistant",
                message=message,
            )

        )

        memory.touch()

    # ---------------------------------------------------------

    def update_filters(
        self,
        memory: ConversationMemory,
        filters: dict[str, Any],
    ) -> None:
        """
        Merge new filters with existing ones.
        """

        if not filters:
            return

        memory.filters.update(filters)

        memory.touch()

    # ---------------------------------------------------------

    def remove_filter(
        self,
        memory: ConversationMemory,
        key: str,
    ) -> None:

        memory.filters.pop(key, None)

        memory.touch()

    # ---------------------------------------------------------

    def clear_filters(
        self,
        memory: ConversationMemory,
    ) -> None:

        memory.filters.clear()

        memory.touch()

    # ---------------------------------------------------------

    def set_preferences(
        self,
        memory: ConversationMemory,
        preferences: dict[str, Any],
    ) -> None:

        if not preferences:
            return

        memory.preferences.update(preferences)

        memory.touch()

    # ---------------------------------------------------------

    def set_search_results(
        self,
        memory: ConversationMemory,
        products: list[dict],
    ) -> None:
        """
        Save latest search results.
        """

        memory.last_results = []

        for product in products:

            memory.last_results.append(

                ProductReference(

                    sku=product.get("sku", ""),

                    title=product.get("title", ""),

                    category=product.get("category"),

                    brand=product.get("brand"),

                    price=product.get("price"),

                    metadata=product,
                )

            )

        memory.touch()

    # ---------------------------------------------------------

    def select_product(
        self,
        memory: ConversationMemory,
        product: ProductReference,
    ) -> None:

        if product.sku not in {

            p.sku

            for p in memory.selected_products

        }:

            memory.selected_products.append(product)

            memory.touch()

    # ---------------------------------------------------------

    def set_comparison_products(
        self,
        memory: ConversationMemory,
        products: list[ProductReference],
    ) -> None:

        memory.comparison_products = list(products)

        memory.touch()

    # ---------------------------------------------------------

    def update_planner(
        self,
        memory: ConversationMemory,
        *,
        goal: str | None = None,
        intent: str | None = None,
        tool: str | None = None,
        step: int | None = None,
    ) -> None:

        planner: PlannerState = memory.planner

        if goal is not None:
            planner.active_goal = goal

        if intent is not None:
            planner.current_intent = intent

        if tool is not None:
            planner.last_tool = tool

        if step is not None:
            planner.current_step = step

        memory.touch()

    # ---------------------------------------------------------

    def set_variable(
        self,
        memory: ConversationMemory,
        key: str,
        value: Any,
    ) -> None:

        memory.variables[key] = value

        memory.touch()

    # ---------------------------------------------------------

    def get_variable(
        self,
        memory: ConversationMemory,
        key: str,
        default=None,
    ):

        return memory.variables.get(
            key,
            default,
        )

    # ---------------------------------------------------------

    def summary(
        self,
        memory: ConversationMemory,
    ) -> dict:

        return {

            "history": len(memory.history),

            "filters": memory.filters,

            "preferences": memory.preferences,

            "results": len(memory.last_results),

            "selected_products": len(memory.selected_products),

            "comparison_products": len(memory.comparison_products),

            "planner": {

                "goal": memory.planner.active_goal,

                "intent": memory.planner.current_intent,

                "tool": memory.planner.last_tool,

                "step": memory.planner.current_step,

            },

        }