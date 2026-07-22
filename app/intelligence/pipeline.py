
from .models import EnrichedProduct
from .document_builder import build_search_document

class ProductIntelligencePipeline:
    def __init__(self, registry, executor):
        self.registry=registry
        self.executor=executor

    def enrich(self, product:dict):
        result=self.executor.execute(product,self.registry)
        ep=EnrichedProduct(product=product)
        ep.taxonomy={"family":result.get("family")}
        ep.synonyms=result.get("synonyms",[])
        ep.use_cases=result.get("use_cases",[])
        ep.benefits=result.get("benefits",[])
        ep.keywords=result.get("keywords",[])
        ep.search_document=build_search_document(ep)
        return ep
