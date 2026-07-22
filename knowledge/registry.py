class KnowledgeRegistry:
    def __init__(self,loader,validator): self.loader=loader; self.validator=validator; self.knowledge=None
    def load(self): self.knowledge=self.loader.load(); self.validator.validate(self.knowledge)
    def get(self,name,default=None): return self.knowledge.documents.get(name,default)
