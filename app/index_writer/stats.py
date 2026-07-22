
from dataclasses import dataclass
@dataclass
class IndexStats:
    indexed:int=0
    failed:int=0
    skipped:int=0
