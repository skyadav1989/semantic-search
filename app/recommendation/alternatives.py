
class Alternatives:
    def cheaper(self,results,max_price):
        return [r for r in results if r.get("payload",{}).get("price",0)<=max_price]
