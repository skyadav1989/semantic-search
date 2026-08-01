"""
Shopping Planner

Creates a deterministic execution plan for the Shopping Agent.
"""

from __future__ import annotations

import logging
import re

from .models import (
    AgentPlan,
    ExecutionContext,
    PlanStep,
    PlannerResult,
    ToolType,
)

logger = logging.getLogger(__name__)


class AgentPlanner:
    """
    Rule-based planner.

    Decides which tool(s) should execute.
    """

    FAQ_PATTERN = re.compile(
        r"\b("
        r"what|why|how|difference|compare|"
        r"warranty|return|returns|delivery|shipping|"
        r"installation|install|emi|payment|"
        r"rpm|bldc|sweep|air delivery|"
        r"power consumption|electricity"
        r")\b",
        re.I,
    )

    RECOMMEND_PATTERN = re.compile(
        r"\b("
        r"recommend|suggest|similar|alternative|"
        r"compatible|bundle|matching"
        r")\b",
        re.I,
    )

    SKU_PATTERN = re.compile(
        r"\b[A-Z0-9][A-Z0-9-]{5,}\b",
        re.I,
    )

    # ---------------------------------------------------------

    def plan(
        self,
        *,
        context: ExecutionContext,
        query: str,
        limit: int = 10,
    ) -> PlannerResult:
        """
        Build execution plan.
        """

        query = query.strip()

        logger.info(
            "Planning query: %s",
            query,
        )

        #
        # Save intent later
        #

        #
        # SKU Lookup
        #

        sku = self._extract_sku(query)

        if sku:

            return PlannerResult(
                intent="catalog",
                confidence=0.99,
                plan=AgentPlan(
                    goal=query,
                    steps=[
                        PlanStep(
                            id=1,
                            tool=ToolType.CATALOG,
                            description="Load product by SKU",
                            input={
                                "sku": sku,
                            },
                            reasoning="SKU detected",
                        )
                    ],
                    metadata={
                        "reason": "catalog_lookup",
                    },
                ),
            )

        #
        # FAQ
        #

        if self.FAQ_PATTERN.search(query):

            return PlannerResult(
                intent="faq",
                confidence=0.95,
                plan=AgentPlan(
                    goal=query,
                    steps=[
                        PlanStep(
                            id=1,
                            tool=ToolType.FAQ,
                            description="Answer FAQ",
                            input={
                                "query": query,
                                "limit": limit,
                            },
                            reasoning="FAQ detected",
                        )
                    ],
                    metadata={
                        "reason": "faq",
                    },
                ),
            )

        #
        # Recommendation
        #

        if self.RECOMMEND_PATTERN.search(query):

            return PlannerResult(
                intent="recommendation",
                confidence=0.90,
                plan=AgentPlan(
                    goal=query,
                    steps=[
                        PlanStep(
                            id=1,
                            tool=ToolType.RECOMMENDATION,
                            description="Generate recommendations",
                            input={
                                "query": query,
                                "limit": limit,
                            },
                            reasoning="Recommendation request",
                        )
                    ],
                    metadata={
                        "reason": "recommendation",
                    },
                ),
            )

        #
        # Default Search
        #

        return PlannerResult(
            intent="search",
            confidence=0.85,
            plan=AgentPlan(
                goal=query,
                steps=[
                    PlanStep(
                        id=1,
                        tool=ToolType.SEARCH,
                        description="Search products",
                        input={
                            "query": query,
                            "limit": limit,
                        },
                        reasoning="Default search",
                    )
                ],
                metadata={
                    "reason": "search",
                },
            ),
        )

    # ---------------------------------------------------------

    def _extract_sku(
        self,
        query: str,
    ) -> str | None:

        match = self.SKU_PATTERN.search(query)

        if not match:
            return None

        return match.group(0).upper()