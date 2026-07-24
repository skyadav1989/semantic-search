from __future__ import annotations
import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi
from .tokenizer import BM25Tokenizer

class BM25Indexer:
    """Build and persist a BM25 index."""

    def __init__(self):
        self.tokenizer = BM25Tokenizer()

    def build(self, documents: list[dict], output_file: str):
        corpus = [self.tokenizer.tokenize(d["text"]) for d in documents]
        bm25 = BM25Okapi(corpus)
        data = {"bm25": bm25, "documents": documents}
        output = Path(output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("wb") as f:
            pickle.dump(data, f)
        return output
