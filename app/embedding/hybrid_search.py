from typing import List, Optional

class HybridSearch:
    """
    Hybrid search combining semantic vector search with simple lexical scoring.
    """

    def __init__(self, embedder, qdrant_client, collection_name: str):
        self.embedder = embedder
        self.client = qdrant_client
        self.collection_name = collection_name

    def _lexical_score(self, query: str, text: str) -> float:
        query_terms = set(query.lower().split())
        text_terms = set(text.lower().split())
        if not query_terms:
            return 0.0
        return len(query_terms & text_terms) / len(query_terms)

    def search(
        self,
        query: str,
        limit: int = 10,
        semantic_weight: float = 0.8,
        lexical_weight: float = 0.2,
        filter: Optional[dict] = None
    ) -> List[dict]:

        vector = self.embedder.encode(query)

        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
            query_filter=filter
        )

        results = []

        for item in response:
            payload = item.payload

            lexical = self._lexical_score(
                query,
                payload.get("title", "")
            )

            semantic = float(item.score)

            score = (
                semantic * semantic_weight
                + lexical * lexical_weight
            )

            payload["semantic_score"] = semantic
            payload["lexical_score"] = lexical
            payload["hybrid_score"] = score

            results.append(payload)

        return sorted(
            results,
            key=lambda x: x["hybrid_score"],
            reverse=True
        )
