from typing import Iterable, List, Sequence

class BatchEmbedder:
    """
    Splits text into batches and delegates embedding generation.
    """

    def __init__(self, embedder, batch_size: int = 32):
        self.embedder = embedder
        self.batch_size = batch_size

    def batches(self, items: Sequence[str]):
        for i in range(0, len(items), self.batch_size):
            yield items[i:i+self.batch_size]

    def encode(self, texts: Sequence[str]) -> List[List[float]]:
        vectors = []
        for batch in self.batches(texts):
            vectors.extend(self.embedder.encode_batch(batch))
        return vectors

    def encode_iter(self, texts: Iterable[str]):
        batch=[]
        for text in texts:
            batch.append(text)
            if len(batch)==self.batch_size:
                for vec in self.embedder.encode_batch(batch):
                    yield vec
                batch.clear()
        if batch:
            for vec in self.embedder.encode_batch(batch):
                yield vec
