from app.search.filter_builder import MetadataFilterBuilder

builder = MetadataFilterBuilder()

attributes = {
    "category": "Fans",
    "color": "white",
    "brand": "Havells",
    "max_price": 3000
}

print(builder.build(attributes))
