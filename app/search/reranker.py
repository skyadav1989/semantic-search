"""
Cross Encoder Reranker

Reranks candidates returned from Hybrid Search
using a CrossEncoder model.
"""

from __future__ import annotations

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):

        self.model = CrossEncoder(model_name)

    # ---------------------------------------------------------

    def rerank(
        self,
        query: str,
        candidates: list,
        top_k: int = 20,
    ):

        if not candidates:
            return []

        #
        # Build sentence pairs
        #

        pairs = []

        for candidate in candidates:

            payload = candidate.get("payload", {})

            text = self._build_document(payload)

            pairs.append(
                (
                    query,
                    text,
                )
            )

        #
        # Predict relevance
        #

        scores = self.model.predict(pairs)

        #
        # Attach scores
        #

        for candidate, score in zip(candidates, scores):

            candidate["cross_score"] = float(score)

        #
        # Sort
        #

        candidates.sort(
            key=lambda x: x["cross_score"],
            reverse=True,
        )

        return candidates[:top_k]

    # ---------------------------------------------------------

    def _build_document(
        self,
        payload,
    ):

        parts = [

            payload.get("title", ""),

            payload.get("category", ""),

            payload.get("search_document", ""),

            " ".join(payload.get("keywords", [])),

            " ".join(payload.get("benefits", [])),

            " ".join(payload.get("use_cases", [])),
        ]

        #
        # Generic attributes
        #

        attributes = payload.get(
            "attributes",
            {},
        )

        for key, value in attributes.items():

            parts.append(f"{key} {value}")

        return " ".join(
            str(x)
            for x in parts
            if x
        )