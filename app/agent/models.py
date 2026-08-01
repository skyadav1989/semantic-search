"""
Agent Models

Shared models for the Shopping Agent.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ==========================================================
# ENUMS
# ==========================================================

class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ToolType(str, Enum):
    SEARCH = "search"
    RECOMMENDATION = "recommendation"
    CATALOG = "catalog"
    FAQ = "faq"
    CHAT = "chat"


# ==========================================================
# REQUEST
# ==========================================================

class AgentRequest(BaseModel):
    session_id: str = "default"
    query: str
    limit: int = 10


# ==========================================================
# MEMORY
# ==========================================================

class AgentMemory(BaseModel):
    """
    Working memory shared by all tools.
    """

    query: str = ""

    rewritten_query: str = ""

    intent: str = ""

    filters: dict[str, Any] = Field(default_factory=dict)

    variables: dict[str, Any] = Field(default_factory=dict)

    products: list[dict] = Field(default_factory=list)

    history: list[dict] = Field(default_factory=list)


# ==========================================================
# TOOL EXECUTION
# ==========================================================

class ToolCall(BaseModel):
    tool: ToolType

    input: dict[str, Any] = Field(default_factory=dict)

    reasoning: str = ""


class ToolResult(BaseModel):
    tool: ToolType

    success: bool = True

    data: Any = None

    error: str | None = None


class ExecutionContext(BaseModel):
    """
    Runtime execution context.
    """

    session_id: str

    memory: AgentMemory = Field(
        default_factory=AgentMemory,
    )

    results: list[ToolResult] = Field(
        default_factory=list,
    )


# ==========================================================
# PLANNING
# ==========================================================

class PlanStep(BaseModel):

    id: int

    tool: ToolType

    description: str

    input: dict[str, Any] = Field(
        default_factory=dict,
    )

    reasoning: str = ""

    status: AgentStatus = AgentStatus.PENDING


class AgentPlan(BaseModel):

    goal: str

    steps: list[PlanStep] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class PlannerResult(BaseModel):

    intent: str

    confidence: float = 1.0

    plan: AgentPlan


# ==========================================================
# RESPONSE
# ==========================================================

class AgentResponse(BaseModel):

    answer: str

    plan: AgentPlan

    tool_calls: list[ToolCall] = Field(
        default_factory=list,
    )

    tool_results: list[ToolResult] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )