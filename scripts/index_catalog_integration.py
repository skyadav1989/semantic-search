"""
Example integration for scripts/index_catalog.py

Replace your current processing loop with the snippet below.
"""

from app.catalog.loader import CatalogLoader
from app.knowledge.loader import KnowledgeLoader
from app.knowledge.validator import KnowledgeValidator
from app.knowledge.registry import KnowledgeRegistry
from app.intelligence.models import EnrichedProduct
from app.intelligence.product_intelligence_pipeline import ProductIntelligencePipeline


loader = CatalogLoader("data/normalized")
products = loader.load()

knowledge_loader = KnowledgeLoader("knowledge/v1")
validator = KnowledgeValidator()
registry = KnowledgeRegistry(knowledge_loader, validator)
registry.load()

pipeline = ProductIntelligencePipeline(registry)

enriched_products = []

for p in products:
    enriched = EnrichedProduct(
        sku=p.sku,
        title=p.title,
        category=p.category,
        subcategory=p.subcategory,
        raw=p.raw,
    )
    pipeline.process(enriched)
    enriched_products.append(enriched)

print(f"Enriched {len(enriched_products)} products")
