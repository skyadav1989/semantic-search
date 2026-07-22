from app.intelligence.models import EnrichedProduct

class KeywordBuilder:
    """
    Builds semantic keywords from title/category/subcategory and
    expands them using taxonomy and synonyms from KnowledgeRegistry.
    """

    def __init__(self, registry):
        self.registry = registry
        self.taxonomy = registry.get("taxonomy", {})
        self.synonyms = registry.get("synonyms", {})

    def build(self, product: EnrichedProduct) -> EnrichedProduct:

        keywords = set()

        for value in (product.title, product.category, product.subcategory):
            if value:
                keywords.add(value.strip().lower())

        # taxonomy expansion
        category = product.category.lower()
        node = self.taxonomy.get(category)

        if isinstance(node, dict):
            for v in node.values():
                if isinstance(v, list):
                    keywords.update(str(x).lower() for x in v)
                elif isinstance(v, str):
                    keywords.add(v.lower())

        # synonym expansion
        for word in list(keywords):
            vals = self.synonyms.get(word)
            if isinstance(vals, list):
                keywords.update(str(x).lower() for x in vals)

        product.keywords = sorted(keywords)
        product.synonyms = sorted(
            {s for k in product.keywords
               for s in (self.synonyms.get(k) or [])}
        )
        return product
