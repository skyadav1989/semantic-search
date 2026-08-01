"""
Chat fallback tool.
"""

from __future__ import annotations

from app.agent.models import AgentContext, ToolResult, ToolType


class ChatTool:
    name = ToolType.CHAT

    def run(self, context: AgentContext, tool_input: dict) -> ToolResult:
        return ToolResult(
            tool=self.name,
            success=True,
            answer="I can help you find products, suggest matching items, look up catalog details, and answer shopping questions.",
            data={"query": context.request.query},
        )
