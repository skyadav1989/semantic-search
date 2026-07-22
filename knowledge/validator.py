class KnowledgeValidator:
    REQUIRED=['taxonomy','synonyms']
    def validate(self,k):
        m=[x for x in self.REQUIRED if x not in k.documents]
        if m: raise ValueError('Missing YAML files: '+','.join(m))
