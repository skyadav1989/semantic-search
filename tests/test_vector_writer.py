from app.embedding.vector_writer import VectorWriter

class MockClient:
    def upsert(self, collection_name, points):
        print("Collection:", collection_name)
        print("Points:", len(points))
        for p in points:
            print(p)

writer = VectorWriter(MockClient(), "semantic_products")

count = writer.write([
    ("SKU001", [0.1,0.2,0.3], {"sku":"SKU001","title":"Wall Fan"}),
    ("SKU002", [0.4,0.5,0.6], {"sku":"SKU002","title":"LED Bulb"}),
])

print("Written:", count)
