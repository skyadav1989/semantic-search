
def build_general(ep):
    return "\n".join(filter(None,[ep.product.get("title",""),ep.product.get("description","")," ".join(ep.synonyms)," ".join(ep.benefits)]))

def build_technical(ep):
    attrs=ep.product.get("attributes",{})
    return "\n".join(f"{k}: {v}" for k,v in attrs.items())

def build_intent(ep):
    return "\n".join([" ".join(ep.use_cases)," ".join(ep.keywords)])
