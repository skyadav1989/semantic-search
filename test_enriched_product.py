from app.intelligence import EnrichedProduct

p=EnrichedProduct(
    sku="ABC",
    title="Wall Fan",
    category="Fans",
    subcategory="Wall Fans",
    raw={}
)

print(p)
