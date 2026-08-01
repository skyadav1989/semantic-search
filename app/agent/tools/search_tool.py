"""
Search tool.
"""

from __future__ import annotations

from app.agent.models import AgentContext, ToolResult, ToolType
from .utils import products_from_results


class SearchTool:
    name = ToolType.SEARCH

    def __init__(self, search_service):
        self.search_service = search_service

    def run(self, context: AgentContext, tool_input: dict) -> ToolResult:
        query = tool_input.get("query") or context.request.query
        limit = int(tool_input.get("limit") or context.request.limit)
        data = self.search_service.search(query=query, limit=limit)
        products = products_from_results(data.get("results", []))
        context.memory.last_query = query
        context.memory.last_intent = context.memory.last_intent
        return ToolResult(
            tool=self.name,
            success=True,
            data=data,
            products=products,
        )
