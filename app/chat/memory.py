"""
Conversation Memory

Stores conversation state and user session.

Current Backend:
    In-Memory

Future:
    Redis
    DynamoDB
    PostgreSQL
"""

from __future__ import annotations

import logging
import threading

from .models import (
    Conversation,
    ConversationState,
    UserSession,
)

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Conversation memory manager.
    """

    def __init__(self):

        self._lock = threading.Lock()

        self._sessions: dict[str, ConversationState] = {}

    # ---------------------------------------------------------

    def get(
        self,
        session_id: str,
    ) -> ConversationState:

        with self._lock:

            state = self._sessions.get(
                session_id,
            )

            if state:

                return state

            logger.info(
                "Creating new session : %s",
                session_id,
            )

            state = ConversationState(

                conversation=Conversation(
                    session_id=session_id,
                ),

                user_session=UserSession(
                    session_id=session_id,
                ),
            )

            self._sessions[session_id] = state

            return state

    # ---------------------------------------------------------

    def save(
        self,
        state: ConversationState,
    ) -> None:

        with self._lock:

            self._sessions[
                state.conversation.session_id
            ] = state

    # ---------------------------------------------------------

    def delete(
        self,
        session_id: str,
    ) -> None:

        with self._lock:

            self._sessions.pop(
                session_id,
                None,
            )

    # ---------------------------------------------------------

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return session_id in self._sessions

    # ---------------------------------------------------------

    def clear(self) -> None:

        with self._lock:

            self._sessions.clear()

    # ---------------------------------------------------------

    def session_count(self) -> int:

        return len(self._sessions)

    # ---------------------------------------------------------

    def all_sessions(
        self,
    ) -> list[str]:

        return list(
            self._sessions.keys()
        )

    # ---------------------------------------------------------

    def cleanup(
        self,
    ) -> int:
        """
        Placeholder for future TTL cleanup.

        Redis implementation will remove
        expired sessions automatically.
        """

        return 0