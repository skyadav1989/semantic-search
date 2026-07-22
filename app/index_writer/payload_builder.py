
def build_payload(product:dict,enriched)->dict:
    return {
        "sku": product["sku"],
        "title": product.get("title"),
        "category": product.get("category"),
        "subcategory": product.get("subcategory"),
        "price": product.get("price"),
        "search_document": getattr(enriched,"search_document",""),
        "keywords": getattr(enriched,"keywords",[]),
        "benefits": getattr(enriched,"benefits",[])
    }
