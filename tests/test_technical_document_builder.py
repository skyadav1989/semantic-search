from app.intelligence import EnrichedProduct
from app.intelligence.technical_document_builder import TechnicalDocumentBuilder

product = EnrichedProduct(
    sku="FAN001",
    title="BLDC Wall Fan",
    category="Fans",
    subcategory="Wall Fans",
    raw={
        "attributes":{
            "motor_type":"BLDC",
            "power":"28 W",
            "sweep":"400 mm",
            "air_delivery":"230 CMM"
        }
    }
)

TechnicalDocumentBuilder().build(product)
print(product.technical_document)
