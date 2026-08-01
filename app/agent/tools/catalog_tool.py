"""
Catalog tool.
"""

from __future__ import annotations

from app.agent.models import AgentContext, ToolResult, ToolType
from .utils import product_from_payload


class CatalogTool:
    name = ToolType.CATALOG

    def __init__(self, retriever=None):
        self.retriever = retriever

    def run(self, context: AgentContext, tool_input: dict) -> ToolResult:
        sku = tool_input.get("sku")
        if not sku:
            return ToolResult(tool=self.name, success=False, error="SKU is required.")

        if not self.retriever:
            return ToolResult(tool=self.name, success=False, error="Catalog retriever is not available.")

        product = self.retriever.get_by_sku(sku)
        if not product:
            return ToolResult(tool=self.name, success=False, error=f"Product '{sku}' was not found.")

        summary = product_from_payload(product.get("payload", {}))
        answer = f"{summary.title or summary.sku} is listed in the catalog."
        return ToolResult(
            tool=self.name,
            success=True,
            data={"sku": sku, "product": product.get("payload", {})},
            products=[summary],
            answer=answer,
        )
