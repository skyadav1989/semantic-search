from app.embedding.hybrid_search import HybridSearch

class MockEmbedder:
    def encode(self, text):
        return [0.1,0.2,0.3]

class Point:
    def __init__(self,title,score):
        self.score=score
        self.payload={"title":title}

class MockClient:
    def search(self,**kwargs):
        return [
            Point("Wall Fan BLDC",0.92),
            Point("Ceiling Fan",0.83),
            Point("LED Bulb",0.75)
        ]

search=HybridSearch(
    MockEmbedder(),
    MockClient(),
    "products"
)

for r in search.search("wall fan"):
    print(r)
