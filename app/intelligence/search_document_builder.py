from app.intelligence.models import EnrichedProduct

class SearchDocumentBuilder:
    """Creates a rich search document for embedding."""

    def build(self, product: EnrichedProduct) -> EnrichedProduct:
        parts=[]

        def add(value):
            if not value:
                return
            if isinstance(value,list):
                for v in value:
                    if v:
                        parts.append(str(v))
            else:
                parts.append(str(value))

        add(product.title)
        add(product.category)
        add(product.subcategory)
        add(product.keywords)
        add(product.synonyms)
        add(product.benefits)
        add(product.use_cases)

        raw=product.raw
        add(raw.get("description",""))

        attrs=raw.get("attributes",{})
        for k,v in attrs.items():
            parts.append(f"{k}: {v}")

        # remove duplicates preserving order
        seen=set()
        final=[]
        for p in parts:
            p=p.strip()
            if not p:
                continue
            key=p.lower()
            if key in seen:
                continue
            seen.add(key)
            final.append(p)

        product.search_document="\n".join(final)
        return product
