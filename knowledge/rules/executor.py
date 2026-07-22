class RuleExecutor:
    def __init__(self): self.rules=[]
    def register(self,r): self.rules.append(r)
    def run(self,p,reg):
        for r in self.rules: p=r.apply(p,reg)
        return p
