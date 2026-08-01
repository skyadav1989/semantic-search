"""
Session Store

Stores conversation memory for active shopping sessions.

Current backend:
    In-Memory Dictionary

Future backends:
    Redis
    PostgreSQL
    MongoDB
"""

from __future__ import annotations

import logging

from .memory import ConversationMemory

logger = logging.getLogger(__name__)


class SessionStore:
    """
    Session storage abstraction.

    One ConversationMemory per session.
    """

    def __init__(self):

        self._sessions: dict[str, ConversationMemory] = {}

    # ---------------------------------------------------------

    def get(
        self,
        session_id: str,
    ) -> ConversationMemory:
        """
        Get or create conversation memory.
        """

        memory = self._sessions.get(session_id)

        if memory:
            return memory

        logger.info(
            "Creating session %s",
            session_id,
        )

        memory = ConversationMemory(
            session_id=session_id,
        )

        self._sessions[session_id] = memory

        return memory

    # ---------------------------------------------------------

    def save(
        self,
        memory: ConversationMemory,
    ) -> None:
        """
        Persist session.
        """

        memory.touch()

        self._sessions[
            memory.session_id
        ] = memory

    # ---------------------------------------------------------

    def delete(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a session.
        """

        self._sessions.pop(
            session_id,
            None,
        )

    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all sessions.
        """

        self._sessions.clear()

    # ---------------------------------------------------------

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return session_id in self._sessions

    # ---------------------------------------------------------

    def count(self) -> int:

        return len(
            self._sessions,
        )

    # ---------------------------------------------------------

    def list_sessions(
        self,
    ) -> list[str]:

        return list(
            self._sessions.keys(),
        )

    # ---------------------------------------------------------

    def active_memories(
        self,
    ) -> list[ConversationMemory]:

        return list(
            self._sessions.values(),
        )

    # ---------------------------------------------------------

    def summary(
        self,
        session_id: str,
    ) -> dict:

        memory = self.get(
            session_id,
        )

        return {
            "session_id": memory.session_id,
            "history": len(memory.history),
            "filters": memory.filters,
            "preferences": memory.preferences,
            "results": len(memory.last_results),
            "selected_products": len(memory.selected_products),
            "comparison_products": len(memory.comparison_products),
            "updated_at": memory.updated_at,
        }