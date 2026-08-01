"""
Conversation Memory

Persistent conversational memory for the Shopping Agent.

Responsibilities

- Store conversation history
- Store active filters
- Store user preferences
- Store previous search results
- Store selected products
- Store comparison products
- Store planner state

This module contains only data models.
No business logic should be implemented here.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ----------------------------------------------------------------------
# Conversation
# ----------------------------------------------------------------------


class ConversationTurn(BaseModel):
    """
    Single conversation turn.
    """

    role: str
    message: str
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )


# ----------------------------------------------------------------------
# Product Reference
# ----------------------------------------------------------------------


class ProductReference(BaseModel):
    """
    Lightweight product reference stored in memory.
    """

    sku: str

    title: str = ""

    category: str | None = None

    brand: str | None = None

    price: float | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


# ----------------------------------------------------------------------
# Planner State
# ----------------------------------------------------------------------


class PlannerState(BaseModel):
    """
    Planner execution state.
    """

    active_goal: str = ""

    current_intent: str = ""

    last_tool: str = ""

    current_step: int = 0

    completed_steps: list[int] = Field(
        default_factory=list,
    )


# ----------------------------------------------------------------------
# Conversation Memory
# ----------------------------------------------------------------------


class ConversationMemory(BaseModel):
    """
    Complete conversation memory for one session.
    """

    session_id: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    #
    # Conversation
    #

    history: list[ConversationTurn] = Field(
        default_factory=list,
    )

    #
    # User preferences
    #

    preferences: dict[str, Any] = Field(
        default_factory=dict,
    )

    #
    # Active search filters
    #

    filters: dict[str, Any] = Field(
        default_factory=dict,
    )

    #
    # Current planner state
    #

    planner: PlannerState = Field(
        default_factory=PlannerState,
    )

    #
    # Previous search results
    #

    last_results: list[ProductReference] = Field(
        default_factory=list,
    )

    #
    # User selected products
    #

    selected_products: list[ProductReference] = Field(
        default_factory=list,
    )

    #
    # Products selected for comparison
    #

    comparison_products: list[ProductReference] = Field(
        default_factory=list,
    )

    #
    # Arbitrary variables
    #

    variables: dict[str, Any] = Field(
        default_factory=dict,
    )

    # ---------------------------------------------------------

    def touch(self) -> None:
        """
        Update last modified timestamp.
        """

        self.updated_at = datetime.utcnow()

    # ---------------------------------------------------------

    def add_turn(
        self,
        *,
        role: str,
        message: str,
    ) -> None:
        """
        Append conversation history.
        """

        self.history.append(

            ConversationTurn(
                role=role,
                message=message,
            )

        )

        self.touch()

    # ---------------------------------------------------------

    def clear_results(self) -> None:
        """
        Remove previous search results.
        """

        self.last_results.clear()

        self.touch()

    # ---------------------------------------------------------

    def clear_comparison(self) -> None:
        """
        Remove comparison list.
        """

        self.comparison_products.clear()

        self.touch()

    # ---------------------------------------------------------

    def clear_filters(self) -> None:
        """
        Remove active filters.
        """

        self.filters.clear()

        self.touch()

    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the conversation while keeping the session.
        """

        self.history.clear()

        self.preferences.clear()

        self.filters.clear()

        self.variables.clear()

        self.last_results.clear()

        self.selected_products.clear()

        self.comparison_products.clear()

        self.planner = PlannerState()

        self.touch()