from app.intelligence.models import EnrichedProduct

class BenefitBuilder:
    """Builds customer-facing benefits from feature_benefits knowledge."""

    def __init__(self, registry):
        self.feature_map = registry.get("feature_benefits", {})

    def build(self, product: EnrichedProduct) -> EnrichedProduct:

        benefits = set(product.benefits)

        attrs = product.raw.get("attributes", {})

        for key, value in attrs.items():

            value = str(value).lower()

            if key in self.feature_map:
                mapping = self.feature_map[key]

                if isinstance(mapping, dict):
                    for feature, vals in mapping.items():
                        vals = vals if isinstance(vals, list) else [vals]
                        if any(str(v).lower() in value for v in vals):
                            benefits.add(feature)

                elif isinstance(mapping, list):
                    benefits.update(mapping)

        product.benefits = sorted(benefits)
        return product
