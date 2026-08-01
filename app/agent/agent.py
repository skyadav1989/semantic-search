"""
Shopping Agent

Main orchestration engine with Conversation Memory.
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
        session_store,
        state_manager,
        conversation,
        filter_merger,
    ):
        self.context = context
        self.planner = planner
        self.tool_executor = tool_executor
        self.prompt_builder = prompt_builder
        self.response_parser = response_parser
        self.filter_merger = filter_merger
        self.llm_client = llm_client

        #
        # Conversation
        #
        self.session_store = session_store
        self.state_manager = state_manager
        self.conversation = conversation

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
        # Runtime execution context
        #
        execution_context = self.context.get(
            request.session_id,
        )

        #
        # Clear previous execution results
        #
        execution_context.results.clear()

        #
        # Persistent conversation memory
        #
        memory = self.session_store.get(
            request.session_id,
        )
        logger.info("Memory = %s", memory.model_dump())
        #
        # Save user message
        #
        self.state_manager.add_user_message(
            memory,
            request.query,
        )

        #
        # Resolve follow-up conversation
        #
        resolved_query = self.conversation.resolve(
            memory,
            request.query,
        )

        logger.info(
            "Resolved Query: %s",
            resolved_query,
        )

        #
        # Save current query
        #
        self.context.set_query(
            execution_context,
            resolved_query,
        )

        #
        # Planning
        #
        planner_result = self.planner.plan(
            context=execution_context,
            query=resolved_query,
            limit=request.limit,
        )

        plan = planner_result.plan

        #
        # Save planner state
        #
        self.state_manager.update_planner(
            memory,
            goal=plan.goal,
            intent=planner_result.intent.value,
        )

        logger.info(
            "Execution plan contains %d step(s)",
            len(plan.steps),
        )

        #
        # Execute tools
        #
        tool_calls = []

        for step in plan.steps:

            tool_call = ToolCall(
                tool=step.tool,
                input=step.input,
                reasoning=step.reasoning,
            )

            tool_calls.append(
                tool_call
            )

            self.tool_executor.execute(
                context=execution_context,
                tool_call=tool_call,
            )

        #
        # Store products returned by tools
        #
        for result in execution_context.results:

            if not result.success:
                continue

            products = result.data.get(
                "products",
                [],
            )

            if products:

                self.state_manager.set_search_results(
                    memory,
                    products,
                )

        #
        # Build LLM prompt
        #
        system_prompt, user_prompt = (
            self.prompt_builder.build(
                query=resolved_query,
                context=execution_context,
                plan=plan,
            )
        )

        #
        # Generate answer
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
        # Save assistant response
        #
        self.state_manager.add_assistant_message(
            memory,
            answer,
        )

        #
        # Persist memory
        #
        self.session_store.save(
            memory,
        )

        #
        # Parse response
        #
        response = self.response_parser.parse(
            answer=answer,
            plan=plan,
            tool_calls=tool_calls,
            tool_results=execution_context.results,
        )

        if hasattr(
            response,
            "session_id",
        ):
            response.session_id = request.session_id

        #
        # Save execution context
        #
        self.context.save(
            execution_context,
        )

        return response

    # ---------------------------------------------------------

    def clear(
        self,
        session_id: str,
    ):

        self.context.delete(
            session_id,
        )

        self.session_store.delete(
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

        memory = self.session_store.get(
            session_id,
        )

        #
        # Merge conversational filters
        #

        filters = self.filter_merger.merge(
            memory,
            request.query,
        )

        self.filter_merger.update_memory(
            memory,
            filters,
        )

        #
        # Make filters available to planner/tools
        #

        execution_context.memory.variables[
            "filters"
        ] = filters

        return {
            "execution": self.context.summary(
                execution_context,
            ),
            "conversation": self.session_store.summary(
                session_id,
            ),
        }