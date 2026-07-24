"""
Reciprocal Rank Fusion (RRF)

Combines multiple ranked result lists into a
single ranked list.

Uses SKU as the unique identifier to avoid
duplicate products.
"""

from __future__ import annotations


class ReciprocalRankFusion:

    def __init__(self, k: int = 60):
        self.k = k

    # ---------------------------------------------------------

    def fuse(
        self,
        semantic_results,
        bm25_results,
        top_k: int = 40,
    ):

        fused = {}

        #
        # Process Semantic Search
        #

        self._accumulate(
            fused,
            semantic_results,
            source="semantic",
        )

        #
        # Process BM25 Search
        #

        self._accumulate(
            fused,
            bm25_results,
            source="bm25",
        )

        #
        # Sort by Fusion Score
        #

        ranked = sorted(
            fused.values(),
            key=lambda x: x["rrf_score"],
            reverse=True,
        )

        return ranked[:top_k]

    # ---------------------------------------------------------

    def _accumulate(
        self,
        fused,
        results,
        source,
    ):

        for rank, item in enumerate(results, start=1):

            payload = item.get("payload", {})

            sku = (
                payload.get("sku")
                or item.get("id")
            )

            if sku is None:
                continue

            score = 1.0 / (self.k + rank)

            if sku not in fused:

                fused[sku] = {

                    #
                    # Identity
                    #

                    "id": item.get("id"),
                    "payload": payload,

                    #
                    # Individual Scores
                    #

                    "semantic_score": 0.0,
                    "bm25_score": 0.0,

                    #
                    # Final Score
                    #

                    "rrf_score": 0.0,
                }

            #
            # Save original retrieval score
            #

            if source == "semantic":

                fused[sku]["semantic_score"] = item.get(
                    "score",
                    0,
                )

            else:

                fused[sku]["bm25_score"] = item.get(
                    "score",
                    0,
                )

            #
            # Add RRF contribution
            #

            fused[sku]["rrf_score"] += score
            fused[sku]["score"] = fused[sku]["rrf_score"]

