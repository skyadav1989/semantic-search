from fastapi import datastructures
from fastapi import datastructures
from app.intelligence import attribute_extractor
from app.intelligence import attribute_extractor
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

        #files = files[:1]

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
            p.get("technical_specifications", {}),
            p.get("variations", []),
        )

   

        return {

            #
            # Identity
            #
            "sku": p.get("sku"),

            "title": p.get("title"),

            "category": category,

            "subcategory": subcategory,

            #
            # Description
            #
            "description": self.clean_html(
                p.get("description", "")
            ),


            
            "key_features": p.get(
                "key_features",
                [],
            ),
            #
            # Pricing
            #
            "price": self.get_price(p),

            "mrp": self.get_mrp(p),

            "currency": self.get_currency(p),

            #
            # Brand
            #
            "brand": p.get("brand", ""),

            #
            # Inventory
            #
            "stock_status": p.get(
                "stock_status",
                ""
            ),

            #
            # Attributes
            #
            "attributes": attrs,

            #
            # Search
            #
            "search_document": self.build_search_document(
                p,
                attrs,
            ),

            #
            # Images
            #
            "images": p.get(
                "images",
                [],
            ),

            #
            # URL
            #
            "url": p.get(
                "url",
                "",
            ),
        }

    # -----------------------------------------------------
    # Category
    # -----------------------------------------------------

    def extract_category(self, category: str):

        if ">" in category:
            return category.split(">")[0].strip()

        return category.strip()

    def extract_subcategory(self, category: str):

        parts = [
            x.strip()
            for x in category.split(">")
            if x.strip()
        ]

        if len(parts) >= 2:
            return parts[-1]

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

        # Keep only digits and decimal point
        price = re.sub(r"[^\d.]", "", price)

        if not price:
            return None

        try:
            return float(price)
        except ValueError:
            return None

    # -----------------------------------------------------
# Generic Price Helpers
# -----------------------------------------------------

    def get_price(self, p):

        fields = [

            "price",

            "price_amount",

            "selling_price",

            "special_price",

            "final_price",

        ]

        for field in fields:

            value = p.get(field)

            if value not in (None, "", 0):

                price = self.parse_price(value)

                if price is not None:

                    return price

        return None


    def get_mrp(self, p):

        fields = [

            "old_price",

            "mrp",

            "old_price_amount",

            "regular_price",

            "list_price",

            "original_price",

        ]

        for field in fields:

            value = p.get(field)


            if value not in (None, "", 0):
                #print(field,value)

                price = self.parse_price(value)
                #print("parsed : "+price)

                if price is not None:

                    return price

        #
        # MRP unavailable
        #

        return None

    def get_currency(self, p):

        return (

            p.get("currency")

            or p.get("price_currency")

            or "INR"

        )
    
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

    def normalize_attributes(self, specs, variations):

        attrs = {}

        #
        # Technical Specifications
        #
        for key, value in specs.items():

            if value is None:
                continue

            key_norm = (
                key.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            attrs[key_norm] = value

        #
        # Variations
        #
        for variation in variations:

            name = variation.get("name", "").strip()

            if not name:
                continue

            key = (
                name.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            options = variation.get("options", [])

            if not options:
                continue

            #
            # Store as comma separated string
            #
            attrs[key] = ", ".join(
                str(option).strip()
                for option in options
                if option
            )

        return attrs
    # -----------------------------------------------------
    # Search Document
    # -----------------------------------------------------

    def build_search_document(self, p, attrs):

        text = []

        text.append(p.get("title", ""))

        text.append(p.get("subtitle", ""))

        text.append(p.get("category", ""))

        text.append(
            self.clean_html(
                p.get("description", "")
            )
        )

       
        for feature in p.get("key_features", []):
            text.append(feature)

        #
        # Price
        #

        price = self.get_price(p)

        mrp = self.get_mrp(p)

        if price is not None:
            text.append(f"Selling Price ₹{price:.0f}")

        if mrp is not None:
            text.append(f"MRP ₹{mrp:.0f}")


        #
        # Attributes
        #
        for key, value in attrs.items():

            if value:
                text.append(f"{key} {value}")

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