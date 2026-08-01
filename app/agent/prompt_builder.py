"""
Agent Prompt Builder

Builds prompts for the Shopping Agent.

Inputs

- Original query
- Execution plan
- Tool results
- Execution context

Output

- System Prompt
- User Prompt
"""

from __future__ import annotations

from .models import (
    AgentPlan,
    ExecutionContext,
    ToolResult,
)


SYSTEM_PROMPT = """
You are an intelligent shopping assistant.

You have access to multiple tools.

Rules

1. Answer ONLY using tool results.

2. Never invent products.

3. Never invent specifications.

4. If tool results contain no matching products,
   clearly explain that.

5. If multiple products are available:

   • Recommend the best one.

   • Explain WHY.

   • Mention important specifications.

6. Never mention internal tools.

7. Be concise.

8. If insufficient information exists,
   say so.
""".strip()


class AgentPromptBuilder:
    """
    Builds prompts for LLM.
    """

    # ---------------------------------------------------------

    def build(
        self,
        *,
        query: str,
        context: ExecutionContext,
        plan: AgentPlan,
    ) -> tuple[str, str]:

        system_prompt = SYSTEM_PROMPT

        user_prompt = self._build_user_prompt(
            query=query,
            context=context,
            plan=plan,
        )

        return (
            system_prompt,
            user_prompt,
        )

    # ---------------------------------------------------------

    def _build_user_prompt(
        self,
        *,
        query: str,
        context: ExecutionContext,
        plan: AgentPlan,
    ) -> str:

        sections = [

            self._query_section(query),

            self._plan_section(plan),

            self._memory_section(context),

            self._tool_results_section(
                context.results,
            ),
        ]

        return "\n\n".join(
            section
            for section in sections
            if section
        )

    # ---------------------------------------------------------

    def _query_section(
        self,
        query: str,
    ) -> str:

        return (
            "## User Query\n\n"
            f"{query}"
        )

    # ---------------------------------------------------------

    def _plan_section(
        self,
        plan: AgentPlan,
    ) -> str:

        lines = [

            "## Execution Plan",

            f"Goal: {plan.goal}",

            "",
        ]

        for step in plan.steps:

            lines.append(
                f"{step.id}. {step.description}"
            )

        return "\n".join(lines)

    # ---------------------------------------------------------

    def _memory_section(
        self,
        context: ExecutionContext,
    ) -> str:

        memory = context.memory

        lines = [

            "## Context",

            f"Intent: {memory.intent}",

            f"Query: {memory.query}",
        ]

        if memory.filters:

            lines.append("")
            lines.append("Filters:")

            for key, value in memory.filters.items():

                lines.append(
                    f"- {key}: {value}"
                )

        if memory.variables:

            lines.append("")
            lines.append("Variables:")

            for key, value in memory.variables.items():

                lines.append(
                    f"- {key}: {value}"
                )

        return "\n".join(lines)

    # ---------------------------------------------------------

    def _tool_results_section(
        self,
        results: list[ToolResult],
    ) -> str:

        if not results:

            return "## Tool Results\n\nNone"

        lines = [

            "## Tool Results",

        ]

        for result in results:

            lines.append("")
            lines.append(
                f"### {result.tool.value}"
            )

            if not result.success:

                lines.append(
                    f"Error: {result.error}"
                )

                continue

            lines.append(
                self._format_data(
                    result.data,
                )
            )

        return "\n".join(lines)

    # ---------------------------------------------------------

    def _format_data(
        self,
        data,
    ) -> str:

        if data is None:

            return "No data"

        if isinstance(
            data,
            (str, int, float),
        ):

            return str(data)

        if isinstance(
            data,
            dict,
        ):

            lines = []

            for key, value in data.items():

                lines.append(
                    f"{key}: {value}"
                )

            return "\n".join(lines)

        if isinstance(
            data,
            list,
        ):

            lines = []

            for index, item in enumerate(
                data,
                start=1,
            ):

                lines.append(
                    f"{index}. {item}"
                )

            return "\n".join(lines)

        return str(data)