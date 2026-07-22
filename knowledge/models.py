from dataclasses import dataclass,field
from typing import Dict,Any
@dataclass
class Knowledge:
    documents:Dict[str,Any]=field(default_factory=dict)
