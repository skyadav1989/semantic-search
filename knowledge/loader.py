from pathlib import Path
import yaml
from .models import Knowledge
class KnowledgeLoader:
    def __init__(self,directory): self.directory=Path(directory)
    def load(self):
        k=Knowledge()
        for f in self.directory.glob('*.yaml'):
            with open(f,encoding='utf-8') as fp: k.documents[f.stem]=yaml.safe_load(fp) or {}
        return k
