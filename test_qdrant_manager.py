from app.embedding.qdrant_manager import QdrantCollectionManager

manager=QdrantCollectionManager()

name="semantic_products"

created=manager.create(name)

print("Created:",created)
print(manager.info(name))
