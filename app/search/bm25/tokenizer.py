from __future__ import annotations
import re

class BM25Tokenizer:
    """Simple tokenizer for BM25."""

    def tokenize(self, text: str) -> list[str]:
        if not text:
            return []
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", " ", text)
        return text.split()
