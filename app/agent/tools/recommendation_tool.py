"""
Recommendation tool.
"""

from __future__ import annotations

from app.agent.models import AgentContext, ProductSummary, ToolResult, ToolType
from .utils import products_from_results


class RecommendationTool:
    name = ToolType.RECOMMENDATION

    def __init__(self, recommendation_service=None):
        self.recommendation_service = recommendation_service

    def run(self, context: AgentContext, tool_input: dict) -> ToolResult:
        sku = tool_input.get("sku")
        limit = int(tool_input.get("limit") or context.request.limit)
        recommendation_type = tool_input.get("recommendation_type") or "similar"

        if sku and self.recommendation_service:
            results = self.recommendation_service.recommend(
                sku=sku,
                recommendation_type=recommendation_type,
                limit=limit,
            )
            return ToolResult(
                tool=self.name,
                success=True,
                data={"sku": sku, "recommendation_type": recommendation_type},
                products=products_from_results(results),
            )

        products: list[ProductSummary] = list(context.memory.remembered_products[:limit])
        if not products:
            return ToolResult(
                tool=self.name,
                success=False,
                error="Recommendation needs a SKU or previous search results.",
            )

        return ToolResult(
            tool=self.name,
            success=True,
            data={"source": "memory", "recommendation_type": recommendation_type},
            products=products,
        )
