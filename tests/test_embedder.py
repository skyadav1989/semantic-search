from app.embedding import BGEM3Embedder

embedder=BGEM3Embedder()

vector=embedder.encode("BLDC wall fan with silent operation")

print("Dimension:",len(vector))
print(vector[:10])
