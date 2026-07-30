
class RecommendationScorer:
    def score(self,item):
        return float(item.get("business_score",0))+float(item.get("score",0))
