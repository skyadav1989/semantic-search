
class IntentDetector:
    BUY_WORDS={"buy","price","cheap","under","below","best"}

    def detect(self,query:str)->str:
        q=query.lower()
        return "BUY" if any(w in q for w in self.BUY_WORDS) else "SEARCH"
