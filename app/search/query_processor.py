
from .query_normalizer import QueryNormalizer
from .intent_detector import IntentDetector
from .attribute_extractor import AttributeExtractor

class QueryProcessor:
    def __init__(self):
        self.norm=QueryNormalizer()
        self.intent=IntentDetector()
        self.attrs=AttributeExtractor()

    def process(self,query:str):
        q=self.norm.normalize(query)
        return {
            "normalized_query":q,
            "intent":self.intent.detect(q),
            "attributes":self.attrs.extract(q)
        }
