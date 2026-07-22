from typing import Optional

class HybridRetriever:
    """
    Retrieve candidates from Qdrant using query embeddings and optional metadata filters.
    """

    def __init__(self, embedder, client, collection_name:str):
        self.embedder=embedder
        self.client=client
        self.collection_name=collection_name

    def retrieve(self, query:str, limit:int=20, metadata_filter:Optional[object]=None):
        vector=self.embedder.encode(query)

        results=self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=metadata_filter,
            limit=limit
        )

        candidates=[]
        for hit in results:
            candidates.append({
                "id": getattr(hit,"id",None),
                "score": float(hit.score),
                "payload": hit.payload
            })
        return candidates
