from app.search.reranker import CrossEncoderReranker

reranker=CrossEncoderReranker()

candidates=[
    {"score":0.82,"payload":{"title":"Wall Fan BLDC"}},
    {"score":0.95,"payload":{"title":"LED Bulb"}},
    {"score":0.90,"payload":{"title":"Ceiling Fan"}}
]

for item in reranker.rerank("wall fan",candidates):
    print(item)
