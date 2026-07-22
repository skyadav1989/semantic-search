
from app.catalog import CatalogLoader
for p in CatalogLoader("data/normalized"):
    print(p.sku,p.title)
