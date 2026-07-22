
from qdrant_client import QdrantClient


from app.embedding.bge_m3_embedder import BGEM3Embedder
from app.embedding.qdrant_manager import QdrantCollectionManager


client = QdrantClient("http://localhost:6333")


#client.delete_collection("products")


#print(client.get_collections())

embedder = BGEM3Embedder()

dimension = embedder.dimension

manager = QdrantCollectionManager()

manager.create(
    collection="products",
    dimension=dimension,
)
print("Collection created")







from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")

info = client.get_collection("products")

print(info)
print(client.count("products", exact=True))