from app.intelligence.keyword_builder import KeywordBuilder
from app.intelligence.benefit_builder import BenefitBuilder
from app.intelligence.usecase_builder import UseCaseBuilder
from app.intelligence.search_document_builder import SearchDocumentBuilder
from app.intelligence.technical_document_builder import TechnicalDocumentBuilder


class ProductIntelligencePipeline:
    """
    Runs all enrichment builders in sequence.
    """

    def __init__(self, registry):
        self.steps = [
            KeywordBuilder(registry),
            BenefitBuilder(registry),
            UseCaseBuilder(registry),
            SearchDocumentBuilder(),
            TechnicalDocumentBuilder(),
        ]

    def process(self, product):
        for step in self.steps:
            product = step.build(product)
        return product
