"""
LLM Answer Generator

Responsible for generating grounded answers
using retrieved search results.
"""

from __future__ import annotations

import logging

from .context_builder import ContextBuilder
from .llm_client import BaseLLMClient
from .models import ChatResponse
from .prompts import (
    SYSTEM_PROMPT,
    SEARCH_PROMPT,
    RECOMMENDATION_PROMPT,
    COMPARE_PROMPT,
    EXPLANATION_PROMPT,
    FOLLOWUP_PROMPT,
)

logger = logging.getLogger(__name__)


class AnswerGenerator:
    """
    Generates grounded LLM answers.
    """

    def __init__(
        self,
        *,
        llm_client: BaseLLMClient,
        context_builder: ContextBuilder,
    ):
        self.llm_client = llm_client
        self.context_builder = context_builder

    # ---------------------------------------------------------

    def answer(
        self,
        *,
        query: str,
        search_results: list[dict],
        prompt_type: str = "search",
        history: str = "",
    ) -> ChatResponse:
        """
        Generate answer from search results.
        """

        #
        # Build Context
        #
        products, context = self.context_builder.build(
            search_results
        )

        #
        # Prompt
        #
        user_prompt = self._build_prompt(
            prompt_type=prompt_type,
            query=query,
            context=context,
            history=history,
        )

        logger.info(
            "Generating LLM answer using %d products",
            len(products),
        )

        #
        # LLM
        #
        response = self.llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        #
        # Citations
        #
        citations = []

        for product in products:

            citations.append(
                {
                    "sku": product.sku,
                    "title": product.title,
                    "url": product.url,
                }
            )

        return ChatResponse(
            query=query,
            answer=response.answer,
            products=products,
            citations=citations,
            metadata={
                "provider": response.provider,
                "model": response.model,
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
            },
        )

    # ---------------------------------------------------------

    def _build_prompt(
        self,
        *,
        prompt_type: str,
        query: str,
        context: str,
        history: str = "",
    ) -> str:

        if prompt_type == "recommendation":

            return RECOMMENDATION_PROMPT.format(
                query=query,
                context=context,
            )

        if prompt_type == "compare":

            return COMPARE_PROMPT.format(
                context=context,
            )

        if prompt_type == "explanation":

            return EXPLANATION_PROMPT.format(
                query=query,
                context=context,
            )

        if prompt_type == "followup":

            return FOLLOWUP_PROMPT.format(
                history=history,
                query=query,
                context=context,
            )

        #
        # Default Search Prompt
        #
        return SEARCH_PROMPT.format(
            query=query,
            context=context,
        )