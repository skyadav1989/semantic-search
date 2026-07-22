
import json
from pathlib import Path
from app.catalog.loader import CatalogLoader

def test_loader(tmp_path):
    d=tmp_path/"x"; d.mkdir()
    (d/"a.json").write_text(json.dumps({"sku":"S1","title":"T","category":"Fans","subcategory":"Wall"}))
    items=list(CatalogLoader(d))
    assert items[0].sku=="S1"
