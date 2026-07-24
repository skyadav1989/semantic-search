"""
Business Ranker

Applies business scoring after AI reranking.

All weights come from

knowledge/v1/ranking_rules.yaml
"""

from __future__ import annotations


class BusinessRanker:

    def __init__(self, registry):

        self.registry = registry

        ranking = registry.ranking_rules.get(
            "ranking",
            {}
        )

        self.semantic_weight = ranking.get(
            "semantic_weight",
            0.60,
        )

        self.rerank_weight = ranking.get(
            "rerank_weight",
            0.25,
        )

        self.business_weight = ranking.get(
            "business_weight",
            0.15,
        )

    # ---------------------------------------------------------

    def rank(self, candidates):

        if not candidates:
            return []

        results = []

        for item in candidates:

            semantic = float(
                item.get(
                    "score",
                    0.0,
                )
            )

            rerank = float(
                item.get(
                    "rerank_score",
                    semantic,
                )
            )

            #
            # Business Boost
            #

            business = 0.0

            #
            # In stock
            #

            if item.get("stock_status") == "In stock":
                business += 1.0

            #
            # Rating
            #

            if item.get("star_rating"):

                try:

                    business += (
                        float(
                            item["star_rating"]
                        )
                        / 5
                    )

                except Exception:
                    pass

            #
            # Final Score
            #

            final = (

                semantic
                * self.semantic_weight

                +

                rerank
                * self.rerank_weight

                +

                business
                * self.business_weight

            )

            item["business_score"] = round(
                final,
                5,
            )

            results.append(item)

        return sorted(
            results,
            key=lambda x: x["business_score"],
            reverse=True,
        )