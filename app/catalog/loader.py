import json
from pathlib import Path

from .models import Product


class CatalogLoader:

    def __init__(self, input_dir):
        self.input_dir = Path(input_dir)

        self._seen = set()

        self.total_files = 0
        self.loaded = 0
        self.duplicates = 0
        self.invalid = 0
        self.missing_sku = 0

    def __iter__(self):

        for path in self.input_dir.rglob("*.json"):

            self.total_files += 1

            try:

                with open(path, encoding="utf-8") as f:
                    data = json.load(f)

            except Exception as e:

                print(f"[INVALID JSON] {path}")
                print(e)

                self.invalid += 1

                continue

            sku = str(data.get("sku", "")).strip()

            if not sku:

                print(f"[MISSING SKU] {path}")

                self.missing_sku += 1

                continue

            if sku in self._seen:

                print(f"[DUPLICATE SKU] {sku} -> {path}")

                self.duplicates += 1

                continue

            self._seen.add(sku)

            self.loaded += 1

            yield Product.from_dict(data)

    def stats(self):

        return {

            "files": self.total_files,

            "loaded": self.loaded,

            "duplicates": self.duplicates,

            "missing_sku": self.missing_sku,

            "invalid_json": self.invalid

        }

    def print_summary(self):

        print()

        print("=" * 60)

        print("Catalog Summary")

        print("=" * 60)

        print(f"Files Scanned : {self.total_files}")

        print(f"Loaded        : {self.loaded}")

        print(f"Duplicates    : {self.duplicates}")

        print(f"Missing SKU   : {self.missing_sku}")

        print(f"Invalid JSON  : {self.invalid}")

        print("=" * 60)