"""
Semantic Engine

This is the application's root object.

It initializes all shared resources once during application startup.

Nothing outside this class should create embedders,
retrievers or pipelines.
"""

from __future__ import annotations

import logging

from app.search.query_processor import QueryProcessor
from app.search.query_expander import QueryExpander
from app.search.filter_builder import MetadataFilterBuilder

from app.search.hybrid_retriever import HybridRetriever
from app.search.reranker import CrossEncoderReranker
from app.search.business_ranker import BusinessRanker

logger = logging.getLogger(__name__)


class SemanticEngine:
    """
    Root application object.
    """

    def __init__(
        self,
        knowledge_dir="knowledge/v1",
        collection="products",
        device="cpu",
    ):

        self.knowledge_dir = knowledge_dir
        self.collection = collection
        self.device = device

        logger.info("Initializing Semantic Engine...")

        #
        # Query Layer
        #
        self.query_processor = QueryProcessor()
        self.query_expander = QueryExpander()
        self.filter_builder = MetadataFilterBuilder()

        #
        # Store values for now
        #
        self.embedder = None
        self.qdrant = None

        #
        # Retrieval
        #
        self.retriever = HybridRetriever(
            embedder=self.embedder,
            client=self.qdrant,
            collection_name=self.collection,
        )

        self.reranker = CrossEncoderReranker()
        self.business_ranker = BusinessRanker()

        #
        # Temporary placeholders so index_catalog.py doesn't crash
        #
        self.intelligence = None
        self.embedding = None
        self.writer = None

        logger.info("Semantic Engine initialized.")

    @property
    def ready(self) -> bool:
        """
        Engine health.
        """

        return True