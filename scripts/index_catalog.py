from app.bootstrap import engine
import argparse
import re
from pathlib import Path

from app.catalog.loader import CatalogLoader
from app.cli.progress import ProgressReporter
from app.intelligence.models import EnrichedProduct

COLOR_MAP = {
    "espresso brown": "brown",
    "brown": "brown",
    "quartz": "white",
    "pearl white": "white",
    "white": "white",
    "ivory": "white",
    "indigo blue": "blue",
    "blue": "blue",
    "grey": "gray",
    "graphite": "gray",
    "black": "black",
}

def try_import_pipeline(args):
    """
    Initialize indexing pipeline directly.
    """

    engine = {
        "intelligence": None,
        "embedding": None,
        "writer": None,
    }

    try:
        #
        # Knowledge
        #
        from app.knowledge.registry import KnowledgeRegistry

        registry = KnowledgeRegistry(args.knowledge)

        #
        # Intelligence
        #
        from app.intelligence.product_intelligence_pipeline import (
            ProductIntelligencePipeline,
        )

        engine["intelligence"] = ProductIntelligencePipeline(
            registry
        )

        #
        # Embedder
        #
        from app.embedding.bge_m3_embedder import BGEM3Embedder

        engine["embedding"] = BGEM3Embedder(
            device=args.device,
        )

        #
        # Vector Writer
        #
        from qdrant_client import QdrantClient
        from app.embedding.vector_writer import VectorWriter

        client = QdrantClient(
            url="http://localhost:6333"
        )

        engine["writer"] = VectorWriter(
            client=client,
            collection_name=args.collection,
        )

        print("✓ Indexing pipeline initialized")

    except Exception as e:
        print(f"[PIPELINE] {e}")

    return engine

def parse_price(value):
    """
    Convert:
        ₹ 16 060
        ₹ 4 800.00
        4800
        None
    into float.
    """

    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value)

    # Keep only digits and decimal point
    value = re.sub(r"[^\d.]", "", value)

    if not value:
        return 0.0

    try:
        return float(value)
    except ValueError:
        return 0.0

def extract_color(raw):
    for variation in raw.get("variations", []):
        if variation.get("name", "").lower() == "colour":
            options = variation.get("options", [])
            if options:
                return options[0].lower()

    return ""


def main():

    parser = argparse.ArgumentParser(
        description="Semantic Engine Catalog Indexer"
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--knowledge", default="knowledge/v1")
    parser.add_argument("--collection", default="products")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        raise FileNotFoundError(input_path)

    print("=" * 60)
    print("Semantic Engine")
    print("=" * 60)

    reporter = ProgressReporter()

    loader = CatalogLoader(input_path)

    engine = try_import_pipeline(args)

    total = 0

    for product in loader:

        total += 1

        reporter.tick()

        if args.dry_run:
            continue

        #
        # Intelligence
        #


        enriched = EnrichedProduct(
            sku=product.sku,
            title=product.title,
            category=product.category,
            subcategory=product.subcategory,
            raw=product.raw,
        )

        if engine["intelligence"]:

            try:
                enriched = engine["intelligence"].process(
                    enriched
                )
            except Exception as e:

                print(f"[INTELLIGENCE] {product.sku}: {e}")

                continue
            

        #
        # Embedding
        #

        bundle = enriched

        if engine["embedding"]:

            try:

                bundle = engine["embedding"].encode(
                    enriched.search_document
                )

            except Exception as e:

                print(f"[EMBEDDING] {product.sku}: {e}")

                continue

        #
        # Index
        #

        if engine["writer"]:

            try:

                payload = {
                    "sku": product.sku,
                    "title": product.title,
                    "category": product.category,
                    "subcategory": product.subcategory,
                    "color": extract_color(product.raw),

                    # Price
                    "price": parse_price(product.raw.get("price_amount")),
                    "mrp": parse_price(product.raw.get("old_price")),

                    # Inventory
                    "stock_status": product.raw.get("stock_status", ""),

                    # Brand
                    "brand": product.raw.get("brand", ""),

                    # Product URL
                    "url": product.raw.get("url", ""),

                    # Primary Image
                    "image": (
                        product.raw.get("images", [None])[0]
                        if product.raw.get("images")
                        else ""
                    ),

                    # Search fields
                    "keywords": enriched.keywords,
                    "benefits": enriched.benefits,
                    "use_cases": enriched.use_cases,

                    "search_document": enriched.search_document,
                    "technical_document": enriched.technical_document,
                }

                engine["writer"].write(
                    [
                        (
                            product.sku,
                            bundle,
                            payload,
                        )
                    ]
                )

            except Exception as e:

                print(f"[INDEX] {product.sku}: {e}")

                continue

    reporter.finish()

    if hasattr(loader, "print_summary"):
        loader.print_summary()

    print(f"\nProducts Loaded : {total}")


if __name__ == "__main__":
    main()