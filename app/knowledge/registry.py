from app.knowledge.loader import KnowledgeLoader


class KnowledgeRegistry:
    """
    Thin wrapper around loaded knowledge documents.
    """

    def __init__(self, directory):
        self.loader = KnowledgeLoader(directory)
        self.knowledge = self.loader.load()

    def get(self, key, default=None):
        return self.knowledge.documents.get(key, default)