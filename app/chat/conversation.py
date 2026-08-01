"""
Conversation Manager

Maintains conversation history for each session.

Responsibilities

- Add user messages
- Add assistant messages
- Retrieve recent history
- Clear history
- Limit conversation size
"""

from __future__ import annotations

import time
import logging

from .models import (
    ChatMessage,
    ConversationState,
)

logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manages conversation history.
    """

    DEFAULT_HISTORY = 20

    def __init__(
        self,
        max_history: int = DEFAULT_HISTORY,
    ):
        self.max_history = max_history

    # ---------------------------------------------------------

    def add_user_message(
        self,
        state: ConversationState,
        message: str,
    ) -> None:

        self._append(
            state,
            role="user",
            content=message,
        )

    # ---------------------------------------------------------

    def add_assistant_message(
        self,
        state: ConversationState,
        message: str,
    ) -> None:

        self._append(
            state,
            role="assistant",
            content=message,
        )

    # ---------------------------------------------------------

    def _append(
        self,
        state: ConversationState,
        *,
        role: str,
        content: str,
    ) -> None:

        state.conversation.messages.append(

            ChatMessage(
                role=role,
                content=content,
                timestamp=time.time(),
            )

        )

        #
        # Keep only latest messages
        #
        if len(state.conversation.messages) > self.max_history:

            state.conversation.messages = (
                state.conversation.messages[-self.max_history :]
            )

    # ---------------------------------------------------------

    def history(
        self,
        state: ConversationState,
    ) -> list[ChatMessage]:

        return state.conversation.messages

    # ---------------------------------------------------------

    def formatted_history(
        self,
        state: ConversationState,
        limit: int = 10,
    ) -> str:
        """
        Convert conversation into text
        for LLM prompt.
        """

        messages = state.conversation.messages[-limit:]

        lines = []

        for message in messages:

            role = (
                "User"
                if message.role == "user"
                else "Assistant"
            )

            lines.append(
                f"{role}: {message.content}"
            )

        return "\n".join(lines)

    # ---------------------------------------------------------

    def last_user_message(
        self,
        state: ConversationState,
    ) -> str | None:

        for message in reversed(
            state.conversation.messages
        ):

            if message.role == "user":

                return message.content

        return None

    # ---------------------------------------------------------

    def last_assistant_message(
        self,
        state: ConversationState,
    ) -> str | None:

        for message in reversed(
            state.conversation.messages
        ):

            if message.role == "assistant":

                return message.content

        return None

    # ---------------------------------------------------------

    def message_count(
        self,
        state: ConversationState,
    ) -> int:

        return len(
            state.conversation.messages
        )

    # ---------------------------------------------------------

    def clear(
        self,
        state: ConversationState,
    ) -> None:

        state.conversation.messages.clear()

        logger.info(
            "Conversation cleared: %s",
            state.conversation.session_id,
        )