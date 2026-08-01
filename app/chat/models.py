"""
Chat Models

Shared models used by the conversational shopping assistant.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


# ==========================================================
# Product
# ==========================================================


class ProductReference(BaseModel):
    """
    Lightweight product reference stored in conversation.
    """

    sku: str

    title: str

    category: str | None = None

    subcategory: str | None = None

    brand: str | None = None

    price: float | None = None

    url: str | None = None

    image: str | None = None


# ==========================================================
# Search Context
# ==========================================================


class SearchContext(BaseModel):
    """
    Current search context.
    """

    query: str = ""

    normalized_query: str = ""

    filters: dict[str, Any] = Field(default_factory=dict)

    attributes: dict[str, Any] = Field(default_factory=dict)

    intent: str = ""

    products: list[ProductReference] = Field(default_factory=list)


# ==========================================================
# Chat Message
# ==========================================================


class ChatMessage(BaseModel):
    """
    Single conversation message.
    """

    role: str

    content: str

    timestamp: float | None = None


# ==========================================================
# Conversation
# ==========================================================


class Conversation(BaseModel):
    """
    Conversation history.
    """

    session_id: str

    messages: list[ChatMessage] = Field(default_factory=list)

    search_context: SearchContext = Field(
        default_factory=SearchContext
    )


# ==========================================================
# User Session
# ==========================================================


class UserSession(BaseModel):
    """
    User preferences remembered during chat.
    """

    session_id: str

    preferred_brand: str | None = None

    preferred_category: str | None = None

    preferred_color: str | None = None

    preferred_budget: float | None = None

    preferred_size: str | None = None


# ==========================================================
# Chat Request
# ==========================================================


class ChatRequest(BaseModel):

    session_id: str

    query: str

    limit: int = 10


# ==========================================================
# Chat Response
# ==========================================================


class ChatResponse(BaseModel):

    session_id: str

    answer: str

    products: list[ProductReference] = Field(default_factory=list)

    filters: dict[str, Any] = Field(default_factory=dict)

    follow_up_questions: list[str] = Field(default_factory=list)


# ==========================================================
# Conversation State
# ==========================================================


class ConversationState(BaseModel):
    """
    Current state of conversation.
    """

    conversation: Conversation

    user_session: UserSession
