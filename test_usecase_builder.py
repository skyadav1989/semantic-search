from app.knowledge.loader import KnowledgeLoader
from app.knowledge.validator import KnowledgeValidator
from app.knowledge.registry import KnowledgeRegistry

from app.intelligence import EnrichedProduct
from app.intelligence.usecase_builder import UseCaseBuilder

loader=KnowledgeLoader("knowledge/v1")
validator=KnowledgeValidator()

registry=KnowledgeRegistry(loader,validator)
registry.load()

builder=UseCaseBuilder(registry)

product=EnrichedProduct(
    sku="TEST001",
    title="Wall Fan",
    category="Fans",
    subcategory="Wall Fans",
    raw={}
)

builder.build(product)

print("Use Cases:")

for u in product.use_cases:
    print("-",u)
