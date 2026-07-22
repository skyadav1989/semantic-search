from typing import Iterable, List
import hashlib

try:
    from qdrant_client.models import PointStruct
except ImportError:
    PointStruct = None


class VectorWriter:
    """
    Bulk upsert vectors into a Qdrant collection.
    """

    def __init__(self, client, collection_name: str):
        self.client = client
        self.collection_name = collection_name

    

    def build_point(self, point_id, vector, payload):
        """
        Convert SKU into a deterministic integer ID for Qdrant.
        """

        qdrant_id = int(
            hashlib.md5(
                str(point_id).encode("utf-8")
            ).hexdigest()[:15],
            16,
        )

        payload["sku"] = str(point_id)

        if PointStruct is None:
            return {
                "id": qdrant_id,
                "vector": vector,
                "payload": payload,
            }

        return PointStruct(
            id=qdrant_id,
            vector=vector,
            payload=payload,
        )

    def write(self, items: Iterable):
        points: List = []

        for point_id, vector, payload in items:
            points.append(
                self.build_point(point_id, vector, payload)
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return len(points)
