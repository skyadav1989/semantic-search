
import re

class QueryNormalizer:
    def normalize(self, query:str)->str:
        query=query.lower().strip()
        query=re.sub(r'\s+',' ',query)
        return query
