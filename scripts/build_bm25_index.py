"""
Build BM25 Index

Usage:

python -m scripts.build_bm25_index \
    --input data/normalized \
    --output storage/bm25.pkl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.search.bm25.index import BM25Indexer


def iter_products(input_path: Path):
    """
    Iterate over all JSON products.
    """

    for file in input_path.rglob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                yield json.load(f)
        except Exception as e:
            print(f"[ERROR] {file}: {e}")


def build_documents(input_path: Path):

    documents = []

    for product in iter_products(input_path):

        text = (
            product.get("search_document")
            or product.get("description")
            or product.get("title", "")
        )

        documents.append(
            {
                "sku": product.get("sku"),
                "title": product.get("title"),
                "category": product.get("category"),
                "text": text,
            }
        )

    return documents


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
    )

    parser.add_argument(
        "--output",
        default="storage/bm25.pkl",
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        raise FileNotFoundError(input_path)

    print("=" * 60)
    print("Building BM25 Index")
    print("=" * 60)

    documents = build_documents(input_path)

    print(f"Documents : {len(documents)}")

    indexer = BM25Indexer()

    indexer.build(
        documents,
        args.output,
    )

    print(f"Saved : {args.output}")


if __name__ == "__main__":
    main()