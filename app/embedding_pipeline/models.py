
from dataclasses import dataclass

@dataclass
class EmbeddingBundle:
    sku:str
    general_text:str
    technical_text:str
    intent_text:str
    general_vector:list
    technical_vector:list
    intent_vector:list
    manifest:dict
