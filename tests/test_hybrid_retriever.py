from app.search.hybrid_retriever import HybridRetriever

class MockEmbedder:
    def encode(self,q):
        return [0.1,0.2,0.3]

class Hit:
    def __init__(self,id,score,title):
        self.id=id
        self.score=score
        self.payload={"title":title}

class MockClient:
    def search(self,**kwargs):
        print("Query Vector:",kwargs["query_vector"])
        print("Limit:",kwargs["limit"])
        return [
            Hit("SKU001",0.95,"Wall Fan"),
            Hit("SKU002",0.90,"Ceiling Fan"),
        ]

retriever=HybridRetriever(MockEmbedder(),MockClient(),"products")
for r in retriever.retrieve("wall fan",limit=2):
    print(r)
