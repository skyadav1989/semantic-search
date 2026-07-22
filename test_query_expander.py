from app.search.query_expander import QueryExpander

expander = QueryExpander()

queries = [
    "fan",
    "buy fan",
    "led bulb",
    "ac"
]

for q in queries:
    print("="*40)
    print(expander.expand(q))
