from app.knowledge.loader import KnowledgeLoader

loader = KnowledgeLoader("knowledge/v1")
knowledge = loader.load()

print("\nLoaded knowledge sections:")
for k in knowledge.documents:
    print(" -", k)

print("\nVersion:",
      knowledge.documents["_manifest"]["version"])
