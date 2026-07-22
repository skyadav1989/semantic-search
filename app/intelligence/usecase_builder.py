from app.intelligence.models import EnrichedProduct

class UseCaseBuilder:
    """Generates use-cases from category, subcategory and knowledge base."""

    def __init__(self, registry):
        self.usecase_map = registry.get("use_cases", {})

    def build(self, product: EnrichedProduct) -> EnrichedProduct:

        use_cases = set(product.use_cases)

        keys = [
            product.category.lower(),
            product.subcategory.lower(),
            product.title.lower()
        ]

        for key in keys:
            mapping = self.usecase_map.get(key)

            if not mapping:
                continue

            if isinstance(mapping, list):
                use_cases.update(mapping)

            elif isinstance(mapping, dict):
                for values in mapping.values():
                    if isinstance(values, list):
                        use_cases.update(values)
                    elif isinstance(values, str):
                        use_cases.add(values)

            elif isinstance(mapping, str):
                use_cases.add(mapping)

        product.use_cases = sorted(use_cases)

        return product
