
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Product:
    sku:str
    title:str
    category:str
    subcategory:str
    search_document:str=""
    raw:dict[str,Any]=field(default_factory=dict)

    @classmethod
    def from_dict(cls,data:dict):
        return cls(
            sku=data["sku"],
            title=data.get("title",""),
            category=data.get("category",""),
            subcategory=data.get("subcategory",""),
            search_document=data.get("search_document",""),
            raw=data,
        )
