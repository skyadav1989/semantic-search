"""
Agent Response Parser

Converts LLM output into a structured AgentResponse.

Responsibilities

- Normalize answer
- Generate citations
- Extract follow-up questions
- Attach metadata
"""

from __future__ import annotations

import logging

from .models import (
    AgentPlan,
    AgentResponse,
    ToolCall,
    ToolResult,
)

logger = logging.getLogger(__name__)


class AgentResponseParser:
    """
    Parses final agent response.
    """

    DEFAULT_FOLLOWUPS = [

        "Show similar products",

        "Show cheaper options",

        "Show premium options",

        "Only in-stock products",
    ]

    # ---------------------------------------------------------

    def parse(
        self,
        *,
        answer: str,
        plan: AgentPlan,
        tool_calls: list[ToolCall],
        tool_results: list[ToolResult],
    ) -> AgentResponse:
        """
        Build AgentResponse.
        """

        answer = self._normalize_answer(
            answer,
        )

        metadata = self._metadata(
            plan=plan,
            tool_results=tool_results,
        )

        return AgentResponse(

            answer=answer,

            plan=plan,

            tool_calls=tool_calls,

            tool_results=tool_results,

            metadata=metadata,
        )

    # ---------------------------------------------------------

    def _normalize_answer(
        self,
        answer: str,
    ) -> str:

        if not answer:

            return (
                "Sorry, I couldn't generate an answer."
            )

        answer = answer.strip()

        while "\n\n\n" in answer:

            answer = answer.replace(
                "\n\n\n",
                "\n\n",
            )

        return answer

    # ---------------------------------------------------------

    def citations(
        self,
        tool_results: list[ToolResult],
    ) -> list[dict]:
        """
        Generate citations from products.
        """

        citations = []

        seen = set()

        for result in tool_results:

            if not result.success:
                continue

            data = result.data

            if not isinstance(
                data,
                list,
            ):
                continue

            for item in data:

                if not isinstance(
                    item,
                    dict,
                ):
                    continue

                sku = item.get("sku")

                if not sku:
                    continue

                if sku in seen:
                    continue

                seen.add(sku)

                citations.append(
                    {
                        "sku": sku,
                        "title": item.get("title"),
                        "url": item.get("url"),
                    }
                )

        return citations

    # ---------------------------------------------------------

    def followups(
        self,
        tool_results: list[ToolResult],
    ) -> list[str]:

        #
        # Future:
        # Gemini-generated followups
        #

        return list(
            self.DEFAULT_FOLLOWUPS
        )

    # ---------------------------------------------------------

    def _metadata(
        self,
        *,
        plan: AgentPlan,
        tool_results: list[ToolResult],
    ) -> dict:

        success = sum(

            1

            for result in tool_results

            if result.success

        )

        failed = len(tool_results) - success

        return {

            "goal": plan.goal,

            "steps": len(
                plan.steps,
            ),

            "successful_tools": success,

            "failed_tools": failed,
        }

    # ---------------------------------------------------------

    def empty(
        self,
        query: str,
    ) -> AgentResponse:

        plan = AgentPlan(
            goal=query,
        )

        return AgentResponse(

            answer=(
                "No matching products were found."
            ),

            plan=plan,

            tool_calls=[],

            tool_results=[],

            metadata={
                "empty": True,
            },
        )

    # ---------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> AgentResponse:

        plan = AgentPlan(
            goal="",
        )

        return AgentResponse(

            answer=message,

            plan=plan,

            tool_calls=[],

            tool_results=[],

            metadata={
                "error": True,
            },
        )