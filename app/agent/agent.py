"""
Shopping Agent

Main orchestration engine.

Flow

User
 │
 ▼
Planner
 │
 ▼
Execution Plan
 │
 ▼
Tool Executor
 │
 ▼
Execution Context
 │
 ▼
Prompt Builder
 │
 ▼
LLM
 │
 ▼
Response Parser
 │
 ▼
Final Response
"""

from __future__ import annotations

import logging

from .models import (
    AgentRequest,
    AgentResponse,
    ToolCall,
)

logger = logging.getLogger(__name__)


class ShoppingAgent:
    """
    Enterprise Shopping Agent.
    """

    def __init__(
        self,
        *,
        context,
        planner,
        tool_executor,
        prompt_builder,
        response_parser,
        llm_client,
    ):
        self.context = context
        self.planner = planner
        self.tool_executor = tool_executor
        self.prompt_builder = prompt_builder
        self.response_parser = response_parser
        self.llm_client = llm_client

    # ---------------------------------------------------------

    def chat(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        logger.info(
            "Agent request: %s",
            request.query,
        )

        #
        # Load execution context
        #
        execution_context = self.context.get(
            request.session_id,
        )
        execution_context.results.clear()
        #
        # Save current query
        #
        self.context.set_query(
            execution_context,
            request.query,
        )

        #
        # Planning
        #
        planner_result = self.planner.plan(
            context=execution_context,
            query=request.query,
            limit=request.limit,
        )

        plan = planner_result.plan

        #
        # Save detected intent
        #
        self.context.set_intent(
            execution_context,
            planner_result.intent,
        )

        logger.info(
            "Execution plan contains %d step(s)",
            len(plan.steps),
        )

        #
        # Execute plan
        #
        tool_calls: list[ToolCall] = []

        for step in plan.steps:

            tool_call = ToolCall(
                tool=step.tool,
                input=step.input,
                reasoning=step.reasoning,
            )

            tool_calls.append(tool_call)

            self.tool_executor.execute(
                context=execution_context,
                tool_call=tool_call,
            )

        #
        # Build prompt
        #
        system_prompt, user_prompt = (
            self.prompt_builder.build(
                query=request.query,
                context=execution_context,
                plan=plan,
            )
        )

        #
        # Generate LLM response
        #
        llm_response = self.llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        answer = getattr(
            llm_response,
            "answer",
            str(llm_response),
        )

        #
        # Build final response
        #
        response = self.response_parser.parse(
            answer=answer,
            plan=plan,
            tool_calls=tool_calls,
            tool_results=execution_context.results,
        )

        #
        # Attach session id (if supported by model)
        #
        if hasattr(response, "session_id"):
            response.session_id = request.session_id

        #
        # Save updated context
        #
        self.context.save(
            execution_context,
        )

        return response

    # ---------------------------------------------------------

    def clear(
        self,
        session_id: str,
    ) -> None:

        self.context.delete(
            session_id,
        )

    # ---------------------------------------------------------

    def session(
        self,
        session_id: str,
    ) -> dict:

        execution_context = self.context.get(
            session_id,
        )

        return self.context.summary(
            execution_context,
        )