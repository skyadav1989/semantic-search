"""
Conversation Resolver

Resolves follow-up shopping queries using conversation memory.

Examples

User:
Best ceiling fan under 5000

↓

User:
Only BLDC

↓

Resolved Query:
Best ceiling fan under 5000 only BLDC


User:
Compare first two

↓

Resolved:
Compare SKU1 and SKU2
"""

from __future__ import annotations

import logging
import re

from .memory import ConversationMemory

logger = logging.getLogger(__name__)


class ConversationResolver:
    """
    Resolves conversational references.
    """

    FOLLOWUP_WORDS = {
        "only",
        "compare",
        "cheaper",
        "costlier",
        "expensive",
        "first",
        "second",
        "third",
        "these",
        "those",
        "them",
        "it",
        "this",
        "that",
        "same",
        "similar",
        "remove",
        "exclude",
        "instead",
    }

    # ---------------------------------------------------------

    def is_followup(
        self,
        query: str,
    ) -> bool:
        """
        Detect if query depends on previous context.
        """

        query = query.lower()

        if not query:
            return False

        words = set(
            re.findall(
                r"\w+",
                query,
            )
        )

        return bool(
            words & self.FOLLOWUP_WORDS
        )

    # ---------------------------------------------------------

    def resolve(
        self,
        memory: ConversationMemory,
        query: str,
    ) -> str:
        """
        Resolve conversational references.
        """

        if not self.is_followup(query):
            return query

        resolved = query

        #
        # Merge previous filters
        #

        if memory.filters:

            filter_text = " ".join(

                f"{k}:{v}"

                for k, v in memory.filters.items()

            )

            resolved = f"{resolved} {filter_text}"

        #
        # Add previous search context
        #

        if memory.last_results:

            titles = [

                product.title

                for product in memory.last_results[:5]

            ]

            resolved += (
                "\n\nPrevious Products:\n"
                + "\n".join(titles)
            )

        logger.info(
            "Resolved Query:\n%s",
            resolved,
        )

        return resolved

    # ---------------------------------------------------------

    def resolve_comparison(
        self,
        memory: ConversationMemory,
        query: str,
    ) -> list[str]:
        """
        Resolve product comparison references.

        Example

        Compare first two

        →

        [SKU1, SKU2]
        """

        query = query.lower()

        products = memory.last_results

        if len(products) < 2:
            return []

        if "first two" in query:

            return [

                products[0].sku,

                products[1].sku,

            ]

        if "first" in query:

            return [

                products[0].sku,

            ]

        if "second" in query:

            return [

                products[1].sku,

            ]

        return []

    # ---------------------------------------------------------

    def resolve_product_reference(
        self,
        memory: ConversationMemory,
        query: str,
    ) -> str | None:
        """
        Resolve

        this

        it

        that

        first one
        """

        query = query.lower()

        if not memory.last_results:
            return None

        if "first" in query:

            return memory.last_results[0].sku

        if (
            "second" in query
            and len(memory.last_results) > 1
        ):

            return memory.last_results[1].sku

        if any(

            word in query

            for word in [

                "this",
                "that",
                "it",

            ]

        ):

            return memory.last_results[0].sku

        return None