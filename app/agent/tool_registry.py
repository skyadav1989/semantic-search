"""
Tool Registry

Central registry for all agent tools.

Responsibilities

- Register tools
- Lookup tools
- Validate availability
- List registered tools
"""

from __future__ import annotations

import logging

from .models import ToolType

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Registry of all agent tools.
    """

    def __init__(self):

        self._tools: dict[ToolType, object] = {}

    # ---------------------------------------------------------

    def register(
        self,
        tool_type: ToolType,
        tool: object,
    ) -> None:
        """
        Register a tool.
        """

        self._tools[tool_type] = tool

        logger.info(
            "Registered tool: %s",
            tool_type.value,
        )

    # ---------------------------------------------------------

    def unregister(
        self,
        tool_type: ToolType,
    ) -> None:
        """
        Remove tool.
        """

        self._tools.pop(
            tool_type,
            None,
        )

    # ---------------------------------------------------------

    def get(
        self,
        tool_type: ToolType,
    ):
        """
        Return registered tool.
        """

        tool = self._tools.get(
            tool_type,
        )

        if tool is None:

            raise ValueError(
                f"Tool '{tool_type.value}' is not registered."
            )

        return tool

    # ---------------------------------------------------------

    def exists(
        self,
        tool_type: ToolType,
    ) -> bool:

        return tool_type in self._tools

    # ---------------------------------------------------------

    def registered_tools(
        self,
    ) -> list[str]:

        return sorted(
            tool.value
            for tool in self._tools.keys()
        )

    # ---------------------------------------------------------

    def count(
        self,
    ) -> int:

        return len(self._tools)

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._tools.clear()

    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "count": self.count(),

            "tools": self.registered_tools(),
        }

    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Ensure required tools exist.
        """

        required = {

            ToolType.SEARCH,

            ToolType.RECOMMENDATION,

        }

        missing = [

            tool.value

            for tool in required

            if tool not in self._tools

        ]

        if missing:

            raise RuntimeError(

                "Missing required tools: "

                + ", ".join(missing)

            )

    # ---------------------------------------------------------

    def __contains__(
        self,
        tool_type: ToolType,
    ) -> bool:

        return tool_type in self._tools

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._tools,
        )

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(
            self._tools.items(),
        )