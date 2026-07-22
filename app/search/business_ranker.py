from typing import List

class BusinessRanker:
    """
    Applies business-specific boosts to search results.
    """

    def __init__(
        self,
        bestseller_boost=0.10,
        in_stock_boost=0.05,
        rating_weight=0.02,
        new_arrival_boost=0.03,
    ):
        self.bestseller_boost = bestseller_boost
        self.in_stock_boost = in_stock_boost
        self.rating_weight = rating_weight
        self.new_arrival_boost = new_arrival_boost

    def score(self, product: dict) -> float:
        score = product.get("rerank_score", product.get("score", 0.0))

        if product.get("is_bestseller"):
            score += self.bestseller_boost

        if product.get("in_stock"):
            score += self.in_stock_boost

        if product.get("is_new_arrival"):
            score += self.new_arrival_boost

        rating = float(product.get("rating", 0))
        score += rating * self.rating_weight

        return score

    def rank(self, products: List[dict]) -> List[dict]:
        for product in products:
            product["business_score"] = self.score(product)

        return sorted(
            products,
            key=lambda p: p["business_score"],
            reverse=True
        )
