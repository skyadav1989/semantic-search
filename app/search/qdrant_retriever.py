"""
Qdrant Retriever

Responsible ONLY for vector retrieval.

Flow

Query
   ↓
Embedder
   ↓
Vector
   ↓
Qdrant
   ↓
Candidates
"""

from __future__ import annotations

import logging
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

try:
    from qdrant_client.models import Filter
except ImportError:
    Filter = Any

logger = logging.getLogger(__name__)


#
# Default payload returned from Qdrant
# Keep this as small as possible.
#
DEFAULT_PAYLOAD = [
    "sku",
    "title",
    "category",
    "subcategory",
    "brand",
    "price",
    "mrp",
    "image",
    "url",
    "stock_status",
    "attributes",
]


class QdrantRetriever:
    """
    Semantic vector retriever.
    """

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
    ):
        self.client = client
        self.collection_name = collection_name


    def get_by_sku(
        self,
        sku: str,
    ) -> dict | None:
        """
        Return complete product by SKU.
        Includes vector.
        """

        logger.info(
            "Loading product %s",
            sku,
        )

        sku_filter = Filter(
            must=[
                FieldCondition(
                    key="sku",
                    match=MatchValue(value=sku),
                )
            ]
        )

        try:

            response = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=sku_filter,
                limit=1,
                with_payload=True,
                with_vectors=True,
            )

            points = response[0]

        except Exception:

            logger.exception(
                "Unable to load SKU %s",
                sku,
            )

            return None

        if not points:
            return None

        point = points[0]

        return {
            "id": str(point.id),
            "vector": point.vector,
            "payload": point.payload or {},
        }

    def get_by_sku(
        self,
        sku: str,
    ) -> dict | None:
        """
        Return complete product by SKU.
        Includes vector.
        """

        logger.info(
            "Loading product %s",
            sku,
        )

        sku_filter = Filter(
            must=[
                FieldCondition(
                    key="sku",
                    match=MatchValue(value=sku),
                )
            ]
        )

        try:

            response = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=sku_filter,
                limit=1,
                with_payload=True,
                with_vectors=True,
            )

            points = response[0]

        except Exception:

            logger.exception(
                "Unable to load SKU %s",
                sku,
            )

            return None

        if not points:
            return None

        point = points[0]

        return {
            "id": str(point.id),
            "vector": point.vector,
            "payload": point.payload or {},
        }


    def get_payload_by_sku(
        self,
        sku: str,
    ) -> dict | None:

        product = self.get_by_sku(sku)

        if not product:
            return None

        return product["payload"]

    def get_payload_by_sku(
        self,
        sku: str,
    ) -> dict | None:

        product = self.get_by_sku(sku)

        if not product:
            return None

        return product["payload"]
    # ---------------------------------------------------------

    def retrieve(
        self,
        vector: list[float],
        *,
        limit: int = 20,
        metadata_filter: Filter | None = None,
        include_search_document: bool = False,
    ) -> list[dict]:
        """
        Search vectors in Qdrant.
        """

        if not vector:
            return []

        #
        # Payload selection
        #

        payload = list(DEFAULT_PAYLOAD)

        if include_search_document:
            payload.extend(
                [
                    "search_document",
                    "technical_document",
                    "keywords",
                    "benefits",
                    "use_cases",
                ]
            )

        logger.info(
            "Searching collection '%s'",
            self.collection_name,
        )

        try:

            response = self.client.query_points(
                collection_name=self.collection_name,
                query=vector,
                query_filter=metadata_filter,
                limit=limit,
                with_payload=payload,
                with_vectors=False,
            )

            hits = response.points

        except AttributeError:

            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                query_filter=metadata_filter,
                limit=limit,
                with_payload=payload,
                with_vectors=False,
            )

        results = []

        for hit in hits:

            hit_payload = getattr(hit, "payload", {}) or {}

            results.append(
                {
                    "id": str(hit.id),
                    "score": float(hit.score),
                    "payload": hit_payload,
                }
            )

        logger.info(
            "Retrieved %d candidates",
            len(results),
        )

        return results