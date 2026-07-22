
from .retry import retry
from .stats import IndexStats
from .logger import logger

class IndexWriter:
    def __init__(self,indexing_service):
        self.indexing=indexing_service
        self.stats=IndexStats()

    def write(self,documents):
        for product_id,doc,payload in documents:
            try:
                retry(lambda:self.indexing.index(product_id,doc,payload))
                self.stats.indexed+=1
            except Exception as e:
                logger.exception("Index failed: %s",e)
                self.stats.failed+=1
        return self.stats
