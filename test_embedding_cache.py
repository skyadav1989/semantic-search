from app.embedding.embedding_cache import EmbeddingCache

cache = EmbeddingCache("test_cache.json")

text = "BLDC wall fan"

print("Initially:", cache.has(text))

cache.put(text, [0.1, 0.2, 0.3])
cache.save()

print("After save:", cache.has(text))
print("Vector:", cache.get(text))

cache2 = EmbeddingCache("test_cache.json")

print("Reloaded:", cache2.get(text))

cache2.clear()
