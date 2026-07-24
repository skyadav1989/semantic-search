from __future__ import annotations
import pickle
from .tokenizer import BM25Tokenizer

class BM25Retriever:
    """Retrieve documents using a persisted BM25 index."""

    def __init__(self, index_file: str):
        with open(index_file, "rb") as f:
            data = pickle.load(f)
        self.bm25 = data["bm25"]
        self.documents = data["documents"]
        self.tokenizer = BM25Tokenizer()

    def retrieve(self, query: str, top_k: int = 20):
        tokens = self.tokenizer.tokenize(query)
        scores = self.bm25.get_scores(tokens)
        ranked = sorted(zip(self.documents, scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [{**doc, "score": float(score)} for doc, score in ranked]
