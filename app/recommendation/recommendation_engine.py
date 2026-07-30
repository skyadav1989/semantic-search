
from .scorer import RecommendationScorer
from .ranking import RankingEngine
from .business_rules import BusinessRules

class RecommendationEngine:
    def __init__(self):
        self.scorer=RecommendationScorer()
        self.rules=BusinessRules()
        self.ranker=RankingEngine()

    def recommend(self,results):
        items=self.rules.apply(results)
        for r in items:
            r["recommendation_score"]=self.scorer.score(r)
        return self.ranker.rank(items)
