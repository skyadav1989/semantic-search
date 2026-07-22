import hashlib
import json
from pathlib import Path


class EmbeddingCache:
    """
    Persistent embedding cache backed by a JSON file.
    """

    def __init__(self, cache_file="embedding_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache = {}

        if self.cache_file.exists():
            try:
                self.cache = json.loads(
                    self.cache_file.read_text(encoding="utf-8")
                )
            except Exception:
                self.cache = {}

    def _hash(self, text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def has(self, text: str) -> bool:
        return self._hash(text) in self.cache

    def get(self, text: str):
        return self.cache.get(self._hash(text))

    def put(self, text: str, embedding):
        self.cache[self._hash(text)] = embedding

    def save(self):
        self.cache_file.write_text(
            json.dumps(self.cache),
            encoding="utf-8"
        )

    def clear(self):
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
