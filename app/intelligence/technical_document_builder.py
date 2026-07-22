from app.intelligence.models import EnrichedProduct

class TechnicalDocumentBuilder:
    """
    Builds a technical-only document for semantic specification search.
    """

    def build(self, product: EnrichedProduct) -> EnrichedProduct:
        lines = []

        def add(label, value):
            if value is None or value == "":
                return
            lines.append(f"{label}: {value}")

        add("SKU", product.sku)
        add("Title", product.title)
        add("Category", product.category)
        add("Subcategory", product.subcategory)

        attrs = product.raw.get("attributes", {})
        for key in sorted(attrs.keys()):
            add(key, attrs[key])

        product.technical_document = "\n".join(lines)
        return product
