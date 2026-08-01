"""
Shopping Agent Planner

Responsible for:

- Intent Detection
- Follow-up Detection
- Multi-step Planning
- Clarification
"""

from __future__ import annotations

import logging
import re

from .models import (
    ExecutionContext,
    AgentIntent,
    AgentPlan,
    PlanStep,
    PlannerResult,
    ToolType,
)

logger = logging.getLogger(__name__)


class AgentPlanner:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def plan(
        self,
        *,
        context: ExecutionContext,
        query: str,
        limit: int = 10,
    ) -> PlannerResult:

        logger.info(
            "Planning query: %s",
            query,
        )

        query_lower = query.lower()

        #
        # Determine intent
        #

        intent = self._detect_intent(query_lower)

        #
        # Build execution plan
        #

        plan = AgentPlan(
            goal=query,
            intent=intent,
            metadata={
                "reason": intent.value,
            },
        )

        #
        # Product Comparison
        #

        if intent == AgentIntent.RECOMMENDATION:

            plan.steps.append(

                PlanStep(
                    id=1,
                    tool=ToolType.RECOMMENDATION,
                    description="Generate recommendations",
                    reasoning="Recommendation detected",
                    input={
                        "query": query,
                        "limit": limit,
                    },
                )

            )

        #
        # FAQ
        #

        elif intent == AgentIntent.FAQ:

            plan.steps.append(

                PlanStep(
                    id=1,
                    tool=ToolType.FAQ,
                    description="Answer FAQ",
                    reasoning="FAQ detected",
                    input={
                        "query": query,
                        "limit": limit,
                    },
                )

            )

        #
        # Product Search
        #

        else:

            plan.steps.append(

                PlanStep(
                    id=1,
                    tool=ToolType.SEARCH,
                    description="Search products",
                    reasoning="Search detected",
                    input={
                        "query": query,
                        "limit": limit,
                    },
                )

            )

        #
        # Follow-up detection
        #

        if self._is_followup(query_lower):

            plan.metadata["followup"] = True

        return PlannerResult(
            intent=intent,
            confidence=1.0,
            plan=plan,
        )

    # ---------------------------------------------------------

    def _detect_intent(
        self,
        query: str,
    ) -> AgentIntent:

        #
        # Recommendation
        #

        if any(

            word in query

            for word in [

                "best",

                "recommend",

                "suggest",

                "top",

            ]

        ):

            return AgentIntent.RECOMMENDATION

        #
        # FAQ
        #

        if any(

            word in query

            for word in [

                "what",

                "why",

                "how",

                "difference",

                "explain",

                "meaning",

            ]

        ):

            return AgentIntent.FAQ

        #
        # Search
        #

        return AgentIntent.PRODUCT_SEARCH

    # ---------------------------------------------------------

    def _is_followup(
        self,
        query: str,
    ) -> bool:

        return any(

            word in query

            for word in [

                "only",

                "cheaper",

                "costlier",

                "compare",

                "remove",

                "exclude",

                "instead",

                "first",

                "second",

                "third",

                "it",

                "them",

                "this",

                "that",

            ]

        )