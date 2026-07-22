from app.embedding.batch_embedder import BatchEmbedder

class MockEmbedder:
    def encode_batch(self, texts):
        return [[float(len(t))] for t in texts]

texts=[
    "wall fan",
    "ceiling fan",
    "pedestal fan",
    "led bulb",
    "switch"
]

batch=BatchEmbedder(MockEmbedder(), batch_size=2)

vectors=batch.encode(texts)

print("Vectors:")
for t,v in zip(texts,vectors):
    print(t, "->", v)
