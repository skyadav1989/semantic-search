from app.search.business_ranker import BusinessRanker

products = [
    {
        "payload": {"title": "Wall Fan"},
        "rerank_score": 0.88,
        "is_bestseller": True,
        "in_stock": True,
        "rating": 4.6
    },
    {
        "payload": {"title": "Ceiling Fan"},
        "rerank_score": 0.91,
        "in_stock": True,
        "rating": 4.2
    },
    {
        "payload": {"title": "LED Bulb"},
        "rerank_score": 0.93,
        "is_new_arrival": True,
        "rating": 3.9
    }
]

ranker = BusinessRanker()

for item in ranker.rank(products):
    print(item["payload"]["title"], item["business_score"])
