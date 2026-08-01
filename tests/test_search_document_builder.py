from app.intelligence import EnrichedProduct
from app.intelligence.search_document_builder import SearchDocumentBuilder

p=EnrichedProduct(
    sku="TEST001",
    title="Wall Fan",
    category="Fans",
    subcategory="Wall Fans",
    raw={
        "description":"High air delivery fan",
        "attributes":{
            "motor_type":"BLDC",
            "sweep":"400 mm"
        }
    }
)
p.keywords=["wall fan","cooling fan"]
p.synonyms=["air circulation fan"]
p.benefits=["energy efficient","silent operation"]
p.use_cases=["bedroom","office"]

SearchDocumentBuilder().build(p)
print(p.search_document)
