from knowledge.loader import KnowledgeLoader
from knowledge.validator import KnowledgeValidator
from knowledge.registry import KnowledgeRegistry

from app.intelligence import EnrichedProduct
from app.intelligence.product_intelligence_pipeline import ProductIntelligencePipeline

loader=KnowledgeLoader("knowledge/v1")
validator=KnowledgeValidator()
registry=KnowledgeRegistry(loader,validator)
registry.load()

product=EnrichedProduct(
    sku="TEST001",
    title="Wall Fan",
    category="Fans",
    subcategory="Wall Fans",
    raw={
        "description":"High air delivery wall fan",
        "attributes":{
            "motor_type":"BLDC",
            "power":"28 W",
            "sweep":"400 mm"
        }
    }
)

pipeline=ProductIntelligencePipeline(registry)
pipeline.process(product)

print("Keywords:", product.keywords)
print("Benefits:", product.benefits)
print("Use Cases:", product.use_cases)
print("\nSearch Document\n----------------")
print(product.search_document)
print("\nTechnical Document\n-------------------")
print(product.technical_document)
