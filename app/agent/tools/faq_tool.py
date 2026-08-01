"""
FAQ Tool

Retrieves knowledge documents for FAQ queries.

Responsibilities

- Search knowledge base
- Rank documents
- Format LLM context
- Return grounded context

Does NOT call the LLM.
"""
from __future__ import annotations

import logging

from app.agent.models import ExecutionContext

logger = logging.getLogger(__name__)


class FAQTool:
    """
    Knowledge retrieval tool.
    """

    def __init__(
        self,
        *,
        retriever,
        ranker,
        formatter,
        limit: int = 5,
    ):
        self.retriever = retriever
        self.ranker = ranker
        self.formatter = formatter
        self.limit = limit

    # ---------------------------------------------------------

    def execute(
        self,
        *,
        context: ExecutionContext,
        query: str,
        limit: int | None = None,
        **_,
    ) -> dict:
        """
        Execute FAQ search.
        """

        logger.info(
            "FAQ Tool: %s",
            query,
        )

        max_results = limit or self.limit

        #
        # Retrieve knowledge documents
        #
        documents = self.retriever.retrieve(
            query=query,
            limit=max_results,
        )

        #
        # Rank documents
        #
        documents = self.ranker.rank(
            documents,
            limit=max_results,
        )

        #
        # Format LLM context
        #
        formatted_context = self.formatter.format(
            documents,
        )

        metadata = self.formatter.metadata(
            documents,
        )

        sources = self.formatter.sources(
            documents,
        )

        #
        # Store in execution context
        #
        context.memory.variables["faq_documents"] = documents
        context.memory.variables["faq_context"] = formatted_context
        context.memory.variables["faq_sources"] = sources

        logger.info(
            "FAQ Tool returned %d document(s)",
            len(documents),
        )

        return {
            "query": query,
            "documents": documents,
            "context": formatted_context,
            "sources": sources,
            "metadata": metadata,
            "count": len(documents),
        }