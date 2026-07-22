from typing import Iterable, Callable

class IncrementalIndexer:
    """
    Incrementally indexes only new or modified documents.
    """

    def __init__(self, cache, batch_embedder, vector_writer):
        self.cache = cache
        self.batch_embedder = batch_embedder
        self.vector_writer = vector_writer

    def index(self, products: Iterable, text_getter: Callable):
        pending = []
        pending_products = []

        for product in products:
            text = text_getter(product)

            if self.cache.has(text):
                continue

            pending.append(text)
            pending_products.append(product)

        if not pending:
            return 0

        vectors = self.batch_embedder.encode(pending)

        items = []

        for product, text, vector in zip(pending_products, pending, vectors):
            payload = {
                "sku": product["sku"],
                "title": product.get("title", "")
            }

            items.append(
                (
                    product["sku"],
                    vector,
                    payload
                )
            )

            self.cache.put(text, vector)

        self.vector_writer.write(items)
        self.cache.save()

        return len(items)
