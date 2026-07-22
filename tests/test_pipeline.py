
from app.intelligence.models import EnrichedProduct
from app.intelligence.document_builder import build_search_document

def test_document():
    ep=EnrichedProduct(product={"title":"Fan","description":"Desk"})
    ep.synonyms=["wall fan"]
    txt=build_search_document(ep)
    assert "Fan" in txt
