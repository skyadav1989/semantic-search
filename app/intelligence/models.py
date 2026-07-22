from dataclasses import dataclass, field
from typing import Any

@dataclass
class EnrichedProduct:
    sku:str
    title:str
    category:str
    subcategory:str
    raw:dict[str,Any]

    keywords:list[str]=field(default_factory=list)
    synonyms:list[str]=field(default_factory=list)
    benefits:list[str]=field(default_factory=list)
    use_cases:list[str]=field(default_factory=list)

    search_document:str=""
    technical_document:str=""
    intent_document:str=""
