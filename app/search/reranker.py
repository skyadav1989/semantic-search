from typing import List

try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None


class CrossEncoderReranker:
    """
    Cross Encoder reranker.
    """

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L6-v2",
    ):

        self.model = None

        if CrossEncoder:
            self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidates: List[dict],
        top_k: int = 10,
    ):

        if not candidates:
            return []

        #
        # Fallback
        #
        if self.model is None:

            for c in candidates:
                c["rerank_score"] = c.get("score", 0.0)

            return sorted(
                candidates,
                key=lambda x: x["rerank_score"],
                reverse=True,
            )[:top_k]

        pairs = []

        for c in candidates:

            payload = c.get("payload", {})

            pairs.append(
                [
                    query,
                    payload.get("title", ""),
                ]
            )

        scores = self.model.predict(pairs)

        for c, score in zip(candidates, scores):
            c["rerank_score"] = float(score)

        return sorted(
            candidates,
            key=lambda x: x["rerank_score"],
            reverse=True,
        )[:top_k]