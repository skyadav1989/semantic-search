"""
Prompt Builder

Builds grounded prompts for the conversational
shopping assistant.

Responsibilities

- Build system prompt
- Include conversation history
- Include retrieved products
- Include current user query
- Keep prompts deterministic
"""

from __future__ import annotations

from typing import Iterable

from .models import ProductReference


SYSTEM_PROMPT = """
You are an expert shopping assistant.

Rules:

1. Answer ONLY using the provided product information.

2. Never invent specifications.

3. Never recommend products that are not in the context.

4. If the answer is unavailable, clearly say so.

5. Prefer concise answers.

6. When recommending products:
   - explain WHY
   - mention price
   - mention important features

7. Never hallucinate.
""".strip()


class PromptBuilder:
    """
    Builds prompts for Gemini/OpenAI.
    """

    # ---------------------------------------------------------

    def build(
        self,
        *,
        query: str,
        products: Iterable[ProductReference],
        history: str = "",
    ) -> tuple[str, str]:

        system_prompt = SYSTEM_PROMPT

        context = self._product_context(products)

        user_prompt = self._user_prompt(
            query=query,
            history=history,
            context=context,
        )

        return (
            system_prompt,
            user_prompt,
        )

    # ---------------------------------------------------------

    def _user_prompt(
        self,
        *,
        query: str,
        history: str,
        context: str,
    ) -> str:

        parts = []

        if history:

            parts.append(
                "Conversation History:\n"
                + history
            )

        parts.append(
            "Available Products:\n"
            + context
        )

        parts.append(
            "User Question:\n"
            + query
        )

        parts.append(
            """
Answer only from the products above.

If no product matches,
say that clearly.

Do not invent information.
""".strip()
        )

        return "\n\n".join(parts)

    # ---------------------------------------------------------

    def _product_context(
        self,
        products: Iterable[ProductReference],
    ) -> str:

        rows = []

        for i, product in enumerate(products, start=1):

            rows.append(
                self._format_product(
                    i,
                    product,
                )
            )

        return "\n\n".join(rows)

    # ---------------------------------------------------------

    def _format_product(
        self,
        index: int,
        product: ProductReference,
    ) -> str:

        lines = [

            f"Product {index}",

            f"SKU: {product.sku}",

            f"Title: {product.title}",
        ]

        if product.category:

            lines.append(
                f"Category: {product.category}"
            )

        if product.subcategory:

            lines.append(
                f"Subcategory: {product.subcategory}"
            )

        if product.brand:

            lines.append(
                f"Brand: {product.brand}"
            )

        if product.price is not None:

            lines.append(
                f"Price: ₹{product.price}"
            )

        if product.url:

            lines.append(
                f"URL: {product.url}"
            )

        if product.attributes:

            lines.append(
                f"Attributes: {product.attributes}"
            )

        if product.benefits:

            lines.append(
                "Benefits: "
                + ", ".join(product.benefits)
            )

        if product.use_cases:

            lines.append(
                "Use Cases: "
                + ", ".join(product.use_cases)
            )

        if product.technical_specs:

            specs = []

            for key, value in product.technical_specs.items():

                specs.append(
                    f"{key}: {value}"
                )

            lines.append(
                "Technical Specs: "
                + ", ".join(specs)
            )

        return "\n".join(lines)