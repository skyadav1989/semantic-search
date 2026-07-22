import argparse
import json
import re
from pathlib import Path
from typing import Any


class CatalogNormalizer:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.total = 0
        self.success = 0
        self.failed = 0

    # -----------------------------------------------------
    # Public
    # -----------------------------------------------------

    def run(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        files = list(self.input_dir.rglob("*.json"))

        print(f"\nFound {len(files)} product files\n")

        for file in files:
            self.total += 1

            try:
                self.process_file(file)
                self.success += 1

            except Exception as e:
                self.failed += 1
                print(f"[ERROR] {file.name}")
                print(e)
                print()

        print("=" * 60)
        print("Normalization Completed")
        print("=" * 60)
        print(f"Total   : {self.total}")
        print(f"Success : {self.success}")
        print(f"Failed  : {self.failed}")

    # -----------------------------------------------------
    # File Processing
    # -----------------------------------------------------

    def process_file(self, file: Path):

        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        normalized = self.normalize_product(data)

        category = normalized["category"]

        out_dir = self.output_dir / category
        out_dir.mkdir(parents=True, exist_ok=True)

        output_file = out_dir / f"{normalized['sku']}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=2, ensure_ascii=False)

        print(f"✓ {normalized['sku']}")

    # -----------------------------------------------------
    # Product Normalization
    # -----------------------------------------------------

    def normalize_product(self, p: dict[str, Any]) -> dict:

        category = self.extract_category(p.get("category", ""))

        subcategory = self.extract_subcategory(p.get("category", ""))

        attrs = self.normalize_attributes(
            p.get("technical_specifications", {})
        )

        return {

            "sku": p.get("sku"),

            "title": p.get("title"),

            "category": category,

            "subcategory": subcategory,

            "description": self.clean_html(
                p.get("description", "")
            ),

            "price": self.parse_price(
                p.get("price_amount")
            ),

            "currency": p.get(
                "price_currency",
                "INR"
            ),

            "attributes": attrs,

            "search_document": self.build_search_document(
                p,
                attrs
            ),

            "images": p.get(
                "images",
                []
            ),

            "url": p.get(
                "url"
            )

        }

    # -----------------------------------------------------
    # Category
    # -----------------------------------------------------

    def extract_category(self, category: str):

        if ">" in category:
            return category.split(">")[0].strip()

        return category.strip()

    def extract_subcategory(self, category: str):

        if ">" in category:
            return category.split(">")[1].strip()

        return ""

    # -----------------------------------------------------
    # Price
    # -----------------------------------------------------

    def parse_price(self, price):

        if price is None:
            return None

        if isinstance(price, (int, float)):
            return float(price)

        price = str(price)

        price = price.replace(",", "")

        price = price.replace("₹", "")

        price = price.strip()

        if not price:
            return None

        try:
            return float(price)

        except:
            return None

    # -----------------------------------------------------
    # HTML
    # -----------------------------------------------------

    def clean_html(self, text):

        if not text:
            return ""

        text = re.sub("<.*?>", " ", text)

        text = text.replace("&amp;", "&")

        return " ".join(text.split())

    # -----------------------------------------------------
    # Attributes
    # -----------------------------------------------------

    def normalize_attributes(self, specs):

        attrs = {}

        for key, value in specs.items():

            if value is None:
                continue

            key_norm = (
                key.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            attrs[key_norm] = value

        return attrs

    # -----------------------------------------------------
    # Search Document
    # -----------------------------------------------------

    def build_search_document(self, p, attrs):

        text = []

        text.append(p.get("title", ""))

        text.append(p.get("subtitle", ""))

        text.append(p.get("category", ""))

        text.append(self.clean_html(
            p.get("description", "")
        ))

        text.extend(
            p.get("key_features", [])
        )

        for k, v in attrs.items():
            text.append(f"{k} {v}")

        return "\n".join(
            x for x in text if x
        )


# -----------------------------------------------------
# CLI
# -----------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Raw JSON folder"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Normalized output folder"
    )

    args = parser.parse_args()

    CatalogNormalizer(
        Path(args.input),
        Path(args.output)
    ).run()


if __name__ == "__main__":
    main()