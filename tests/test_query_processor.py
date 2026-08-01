
from app.search.query_processor import QueryProcessor

qp=QueryProcessor()
print(qp.process("White silent fan below 3000"))
print(qp.process("Buy black LED bulb under 500"))
