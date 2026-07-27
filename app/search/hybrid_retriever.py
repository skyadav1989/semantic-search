"""
Hybrid Retriever

Runs Semantic Search, BM25 Search, or both depending on runtime flags.
"""

from __future__ import annotations
import logging

logger = logging.getLogger(__name__)


class HybridRetriever:
    def __init__(
        self,
        semantic_retriever,
        bm25_retriever,
    ):
        self.semantic_retriever = semantic_retriever
        self.bm25_retriever = bm25_retriever

    # ---------------------------------------------------------

    def retrieve(
        self,
        *,
        vector,
        query: str,
        metadata_filter=None,
        semantic_limit: int = 30,
        bm25_limit: int = 30,
        enable_semantic: bool = True,
        enable_bm25: bool = True,
    ):
        semantic = []
        bm25 = []


        logger.info("=" * 60)

        if enable_semantic:
            logger.info("Semantic Retriever : RUNNING")
        else:
            logger.info("Semantic Retriever : SKIPPED")

        if enable_bm25:
            logger.info("BM25 Retriever     : RUNNING")
        else:
            logger.info("BM25 Retriever     : SKIPPED")

        logger.info("=" * 60)

        if enable_semantic and self.semantic_retriever is not None:
            semantic = self.semantic_retriever.retrieve(
                vector=vector,
                limit=semantic_limit,
                metadata_filter=metadata_filter,
            )

        if enable_bm25 and self.bm25_retriever is not None:
            keyword = self.bm25_retriever.retrieve(
                query=query,
                top_k=bm25_limit,
            )

            for item in keyword:
                payload = dict(item)
                bm25.append(
                    {
                        "id": payload.get("sku", payload.get("id")),
                        "score": payload.get("score", 0),
                        "payload": payload,
                    }
                )

        return {
            "semantic": semantic,
            "bm25": bm25,
        }
