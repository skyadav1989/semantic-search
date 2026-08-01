from app.embedding.incremental_indexer import IncrementalIndexer
from app.embedding.embedding_cache import EmbeddingCache

class MockBatch:
    def encode(self, texts):
        return [[float(len(t))] for t in texts]

class MockWriter:
    def write(self, items):
        print("Writing", len(items), "vectors")
        for item in items:
            print(item)

products=[
    {"sku":"SKU001","title":"Wall Fan"},
    {"sku":"SKU002","title":"LED Bulb"},
]

cache=EmbeddingCache("incremental_test.json")

indexer=IncrementalIndexer(
    cache,
    MockBatch(),
    MockWriter()
)

count=indexer.index(
    products,
    lambda p: p["title"]
)

print("Indexed:",count)

cache.clear()
