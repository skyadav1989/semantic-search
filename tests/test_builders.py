
from app.embedding_pipeline.builders import build_general

class E:
    product={"title":"Fan","description":"Desk"}
    synonyms=["wall fan"]
    benefits=["quiet"]

def test_general():
    assert "Fan" in build_general(E())
