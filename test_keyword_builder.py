from app.knowledge.loader import KnowledgeLoader
from app.knowledge.validator import KnowledgeValidator
from app.knowledge.registry import KnowledgeRegistry
from app.intelligence import EnrichedProduct
from app.intelligence.keyword_builder import KeywordBuilder

loader=KnowledgeLoader("knowledge/v1")
validator=KnowledgeValidator()
registry=KnowledgeRegistry(loader,validator)
registry.load()

builder=KeywordBuilder(registry)

product=EnrichedProduct(
    sku="TEST001",
    title="Wall Fan",
    category="Fans",
    subcategory="Wall Fans",
    raw={}
)

builder.build(product)

print("\nKeywords")
for k in product.keywords:
    print("-",k)

print("\nSynonyms")
for s in product.synonyms:
    print("-",s)
