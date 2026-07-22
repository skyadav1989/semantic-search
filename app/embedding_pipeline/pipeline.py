
from hashlib import sha256
from .builders import build_general,build_technical,build_intent
from .models import EmbeddingBundle

class EmbeddingIntegrationPipeline:
    def __init__(self, encoder):
        self.encoder=encoder

    def transform(self,enriched):
        g=build_general(enriched)
        t=build_technical(enriched)
        i=build_intent(enriched)
        manifest={
            "sku": enriched.product["sku"],
            "hash": sha256((g+t+i).encode()).hexdigest()
        }
        return EmbeddingBundle(
            sku=enriched.product["sku"],
            general_text=g,
            technical_text=t,
            intent_text=i,
            general_vector=self.encoder.encode(g),
            technical_vector=self.encoder.encode(t),
            intent_vector=self.encoder.encode(i),
            manifest=manifest
        )
