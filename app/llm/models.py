"""
LLM Models

Data models used by the LLM module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------
# Chat
# ---------------------------------------------------------


@dataclass(slots=True)
class ChatMessage:
    """
    Conversation message.
    """

    role: str
    content: str


@dataclass(slots=True)
class ChatRequest:
    """
    Incoming chat request.
    """

    query: str
    limit: int = 10
    history: list[ChatMessage] = field(default_factory=list)


# ---------------------------------------------------------
# Product Context
# ---------------------------------------------------------


@dataclass(slots=True)
class ProductContext:
    """
    Product supplied to the LLM.
    """

    sku: str
    title: str
    category: str = ""
    subcategory: str = ""
    brand: str = ""
    price: float = 0.0
    mrp: float = 0.0
    stock_status: str = ""
    url: str = ""
    image: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)
    benefits: list[str] = field(default_factory=list)
    use_cases: list[str] = field(default_factory=list)
    technical_specs: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------
# Citations
# ---------------------------------------------------------


@dataclass(slots=True)
class Citation:
    """
    Product citation.
    """

    sku: str
    title: str
    url: str


# ---------------------------------------------------------
# LLM Response
# ---------------------------------------------------------


@dataclass(slots=True)
class LLMResponse:
    """
    Raw LLM response.
    """

    answer: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


# ---------------------------------------------------------
# Final API Response
# ---------------------------------------------------------


@dataclass(slots=True)
class ChatResponse:
    """
    Response returned by /chat.
    """

    query: str
    answer: str
    products: list[ProductContext] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)