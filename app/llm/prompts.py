"""
LLM Prompt Templates

All prompts used by the Shopping Assistant.
"""

from __future__ import annotations


# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are an expert AI Shopping Assistant.

Your responsibility is to help customers discover products,
compare them, explain differences and recommend the most
appropriate product.

Rules

1. Answer ONLY from the supplied product context.

2. Never invent products.

3. Never invent specifications.

4. If information is unavailable, explicitly say:

   "The provided product information does not contain that detail."

5. Recommend products only from the supplied context.

6. Use bullet points whenever possible.

7. Keep answers concise and factual.

8. Mention prices whenever available.

9. Mention important advantages.

10. Never hallucinate.
""".strip()


# ---------------------------------------------------------
# Search Prompt
# ---------------------------------------------------------

SEARCH_PROMPT = """
User Question

{query}

Retrieved Products

{context}

Answer the customer's question using ONLY the retrieved products.

Include

• Short answer
• Best recommendation
• Why it is recommended
• Alternative products (if applicable)
""".strip()


# ---------------------------------------------------------
# Recommendation Prompt
# ---------------------------------------------------------

RECOMMENDATION_PROMPT = """
Customer Request

{query}

Candidate Products

{context}

Recommend the best product.

Explain

• Why it is the best choice

• Important features

• Price

• Pros

• Possible alternatives
""".strip()


# ---------------------------------------------------------
# Product Comparison
# ---------------------------------------------------------

COMPARE_PROMPT = """
Compare these products.

{context}

Return

• Summary

• Feature comparison

• Advantages

• Disadvantages

• Which customer should buy each product

Use a markdown table whenever possible.
""".strip()


# ---------------------------------------------------------
# Product Explanation
# ---------------------------------------------------------

EXPLANATION_PROMPT = """
Product

{context}

Customer Question

{query}

Answer using ONLY the supplied product information.

If the answer cannot be found,
say so instead of guessing.
""".strip()


# ---------------------------------------------------------
# Follow-up Conversation
# ---------------------------------------------------------

FOLLOWUP_PROMPT = """
Conversation History

{history}

Retrieved Products

{context}

Current Question

{query}

Answer using the previous conversation and
the retrieved products.

Do not invent facts.
""".strip()


# ---------------------------------------------------------
# Prompt Registry
# ---------------------------------------------------------

PROMPTS = {
    "search": SEARCH_PROMPT,
    "recommendation": RECOMMENDATION_PROMPT,
    "compare": COMPARE_PROMPT,
    "explanation": EXPLANATION_PROMPT,
    "followup": FOLLOWUP_PROMPT,
}