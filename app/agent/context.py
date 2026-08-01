"""
Agent Context

Maintains execution context for the shopping agent.

Responsibilities

- Store working memory
- Store tool outputs
- Store extracted variables
- Store retrieved products
- Reset execution state
"""

from __future__ import annotations

import copy
import logging
from typing import Any

from .models import (
    AgentMemory,
    ExecutionContext,
    ToolResult,
)

logger = logging.getLogger(__name__)


class AgentContext:
    """
    Runtime context shared across all tools.
    """

    def __init__(self):

        self._contexts: dict[str, ExecutionContext] = {}

    # ---------------------------------------------------------

    def get(
        self,
        session_id: str,
    ) -> ExecutionContext:

        context = self._contexts.get(session_id)

        if context:
            return context

        context = ExecutionContext(
            session_id=session_id,
            memory=AgentMemory(),
        )

        self._contexts[session_id] = context

        return context

    # ---------------------------------------------------------

    def save(
        self,
        context: ExecutionContext,
    ) -> None:

        self._contexts[
            context.session_id
        ] = context

    # ---------------------------------------------------------

    def delete(
        self,
        session_id: str,
    ) -> None:

        self._contexts.pop(
            session_id,
            None,
        )

    # ---------------------------------------------------------

    def clear(
        self,
        session_id: str,
    ) -> None:

        context = self.get(session_id)

        context.memory = AgentMemory()

        context.results.clear()

    # ---------------------------------------------------------

    def set_query(
        self,
        context: ExecutionContext,
        query: str,
    ) -> None:

        context.memory.query = query

    # ---------------------------------------------------------

    def set_rewritten_query(
        self,
        context: ExecutionContext,
        query: str,
    ) -> None:

        context.memory.rewritten_query = query

    # ---------------------------------------------------------

    def set_intent(
        self,
        context: ExecutionContext,
        intent: str,
    ) -> None:

        context.memory.intent = intent

    # ---------------------------------------------------------

    def set_filters(
        self,
        context: ExecutionContext,
        filters: dict,
    ) -> None:

        context.memory.filters = copy.deepcopy(filters)

    # ---------------------------------------------------------

    def add_filter(
        self,
        context: ExecutionContext,
        key: str,
        value: Any,
    ) -> None:

        context.memory.filters[key] = value

    # ---------------------------------------------------------

    def set_products(
        self,
        context: ExecutionContext,
        products: list[dict],
    ) -> None:

        context.memory.products = list(products)

    # ---------------------------------------------------------

    def add_variable(
        self,
        context: ExecutionContext,
        name: str,
        value: Any,
    ) -> None:

        context.memory.variables[name] = value

    # ---------------------------------------------------------

    def get_variable(
        self,
        context: ExecutionContext,
        name: str,
        default=None,
    ):

        return context.memory.variables.get(
            name,
            default,
        )

    # ---------------------------------------------------------

    def add_result(
        self,
        context: ExecutionContext,
        result: ToolResult,
    ) -> None:

        context.results.append(result)

    # ---------------------------------------------------------

    def latest_result(
        self,
        context: ExecutionContext,
    ) -> ToolResult | None:

        if not context.results:
            return None

        return context.results[-1]

    # ---------------------------------------------------------

    def results(
        self,
        context: ExecutionContext,
    ) -> list[ToolResult]:

        return context.results

    # ---------------------------------------------------------

    def summary(
        self,
        context: ExecutionContext,
    ) -> dict:

        return {

            "query": context.memory.query,

            "rewritten_query": context.memory.rewritten_query,

            "intent": context.memory.intent,

            "filters": context.memory.filters,

            "variables": context.memory.variables,

            "products": len(
                context.memory.products,
            ),

            "tool_results": len(
                context.results,
            ),
        }

    # ---------------------------------------------------------

    def has_products(
        self,
        context: ExecutionContext,
    ) -> bool:

        return bool(
            context.memory.products,
        )

    # ---------------------------------------------------------

    def has_filters(
        self,
        context: ExecutionContext,
    ) -> bool:

        return bool(
            context.memory.filters,
        )

    # ---------------------------------------------------------

    def has_variable(
        self,
        context: ExecutionContext,
        name: str,
    ) -> bool:

        return name in context.memory.variables