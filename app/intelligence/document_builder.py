
def build_search_document(ep):
    parts=[
        ep.product.get("title",""),
        ep.product.get("description",""),
        " ".join(ep.synonyms),
        " ".join(ep.use_cases),
        " ".join(ep.benefits),
        " ".join(ep.keywords),
    ]
    return "\n".join([p for p in parts if p])
