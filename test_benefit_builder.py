from app.knowledge.loader import KnowledgeLoader
from app.knowledge.validator import KnowledgeValidator
from app.knowledge.registry import KnowledgeRegistry
from app.intelligence import EnrichedProduct
from app.intelligence.benefit_builder import BenefitBuilder

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
        "attributes":{
            "motor_type":"BLDC",
            "speed":"3"
        }
    }
)

builder=BenefitBuilder(registry)
builder.build(product)

print("Benefits:")
for b in product.benefits:
    print("-",b)
