"""
Chat Service

Enterprise conversational shopping assistant.

Flow

User Query
      |
      v
Conversation Memory
      |
      v
Follow-up Detection
      |
      v
Search
      |
      v
Context Update
      |
      v
LLM
      |
      v
Conversation Update
      |
      v
Response
"""

from __future__ import annotations

import logging

from .models import (
    ChatRequest,
    ChatResponse,
    ProductReference,
)

logger = logging.getLogger(__name__)


class ChatService:
    """
    Conversational Shopping Assistant.
    """

    def __init__(
        self,
        *,
        memory,
        conversation,
        followup_detector,
        context_manager,
        prompt_builder,
        response_postprocessor,
        search_service,
        answer_generator,
    ):
        self.memory = memory

        self.conversation = conversation

        self.followup_detector = followup_detector

        self.context_manager = context_manager

        self.prompt_builder = prompt_builder

        self.response_postprocessor = response_postprocessor

        self.search_service = search_service

        self.answer_generator = answer_generator

    # ---------------------------------------------------------

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        state = self.memory.get(
            request.session_id,
        )

        previous_query = (
            self.context_manager.latest_query(
                state.conversation.search_context
            )
        )

        if self.followup_detector.is_followup(
            query=request.query,
            previous_query=previous_query,
        ):
            effective_query = self.followup_detector.merge(
                previous_query=previous_query,
                current_query=request.query,
            )

            logger.info(
                "Follow-up detected"
            )

        else:
            effective_query = request.query

        self.conversation.add_user_message(
            state,
            effective_query,
        )

        search_response = self.search_service.search(
            query=effective_query,
            limit=request.limit,
        )

        products = []

        for item in search_response["results"]:
            payload = item["payload"]

            products.append(
                ProductReference(
                    sku=payload.get("sku", ""),
                    title=payload.get("title", ""),
                    category=payload.get("category"),
                    subcategory=payload.get("subcategory"),
                    brand=payload.get("brand"),
                    price=payload.get("price"),
                    url=payload.get("url"),
                    image=payload.get("image"),
                )
            )

        self.context_manager.update(
            context=state.conversation.search_context,
            query=effective_query,
            normalized_query=search_response["normalized_query"],
            filters=search_response["filters"],
            attributes=search_response["attributes"],
            intent=search_response["intent"],
            products=products,
        )

        history = self.conversation.formatted_history(
            state,
        )

        answer = self.answer_generator.answer(
            query=effective_query,
            search_results=search_response["results"],
            history=history,
        )

        self.conversation.add_assistant_message(
            state,
            answer.answer,
        )

        self.memory.save(
            state,
        )

        response = self.response_postprocessor.process(
            answer=answer.answer,
            products=[
                product.model_dump()
                for product in products
            ],
            citations=getattr(answer, "citations", []),
            metadata=getattr(answer, "metadata", {}),
        )

        return ChatResponse(
            session_id=request.session_id,
            answer=response["answer"],
            products=[
                ProductReference(**product)
                for product in response["products"]
            ],
            filters=search_response["filters"],
            follow_up_questions=response["follow_up_questions"],
        )

    # ---------------------------------------------------------

    def clear(
        self,
        session_id: str,
    ):
        self.memory.delete(
            session_id,
        )

    # ---------------------------------------------------------

    def session(
        self,
        session_id: str,
    ):
        state = self.memory.get(
            session_id,
        )

        return {
            "messages": self.conversation.message_count(
                state,
            ),
            "context": self.context_manager.summary(
                state.conversation.search_context,
            ),
        }
