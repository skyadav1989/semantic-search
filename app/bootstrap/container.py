"""
Application Dependency Container

Creates singleton instances used by the API.
"""

from __future__ import annotations

import logging
import os

from app.embedding.bge_m3_embedder import BGEM3Embedder
from app.embedding.qdrant_manager import QdrantCollectionManager

from app.search.query_processor import QueryProcessor
from app.search.query_expander import QueryExpander
from app.search.filter_builder import MetadataFilterBuilder
from app.search.qdrant_retriever import QdrantRetriever
from app.search.reranker import CrossEncoderReranker
from app.search.business_ranker import BusinessRanker

from app.services.search_service import SearchService

logger = logging.getLogger(__name__)


class Container:
    """
    Application Dependency Container
    """

    def __init__(self):

        logger.info("Initializing Semantic Engine...")

        #
        # Configuration
        #

        self.qdrant_url = os.getenv(
            "QDRANT_URL",
            "http://localhost:6333",
        )

        self.qdrant_api_key = os.getenv(
            "QDRANT_API_KEY",
            None,
        )

        self.collection_name = os.getenv(
            "QDRANT_COLLECTION",
            "products",
        )

        self.embedding_model = os.getenv(
            "EMBEDDING_MODEL",
            "BAAI/bge-m3",
        )

        self.embedding_device = os.getenv(
            "EMBEDDING_DEVICE",
            "cpu",
        )

        #
        # Qdrant
        #

        self.qdrant = QdrantCollectionManager(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )

        #
        # Embedder
        #

        self.embedder = BGEM3Embedder(
            model_name=self.embedding_model,
            device=self.embedding_device,
        )

        #
        # Search Components
        #

        self.query_processor = QueryProcessor()

        self.query_expander = QueryExpander()

        self.filter_builder = MetadataFilterBuilder()

        self.retriever = QdrantRetriever(
            client=self.qdrant.client,
            collection_name=self.collection_name,
        )

        self.reranker = CrossEncoderReranker()

        self.business_ranker = BusinessRanker()

        #
        # Search Service
        #

        self.search_service = SearchService(
            query_processor=self.query_processor,
            query_expander=self.query_expander,
            filter_builder=self.filter_builder,
            embedder=self.embedder,
            retriever=self.retriever,
            reranker=self.reranker,
            business_ranker=self.business_ranker,
        )

        logger.info("Semantic Engine Ready")


#
# Singleton
#

container = Container()