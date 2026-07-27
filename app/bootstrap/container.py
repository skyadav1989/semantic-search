"""
Application Dependency Container

Creates singleton instances used by the API.
"""
from __future__ import annotations

import logging
from pathlib import Path

from app.config import get_settings
from app.embedding.bge_m3_embedder import BGEM3Embedder
from app.embedding.qdrant_manager import QdrantCollectionManager
from app.knowledge.registry import KnowledgeRegistry
from app.search.bm25.retriever import BM25Retriever
from app.search.business_ranker import BusinessRanker
from app.search.filter_builder import MetadataFilterBuilder
from app.search.hybrid_retriever import HybridRetriever
from app.search.qdrant_retriever import QdrantRetriever
from app.search.query_expander import QueryExpander
from app.search.query_processor import QueryProcessor
from app.search.reranker import CrossEncoderReranker
from app.search.rrf import ReciprocalRankFusion
from app.services.search_service import SearchService
from config import settings

logger = logging.getLogger(__name__)


class Container:
    """
    Application Dependency Container
    """

    def __init__(self):
        logger.info("Initializing Semantic Engine...")

        self.settings = get_settings()
        self.search_mode = self.settings.SEARCH_MODE.lower().strip()

        self.enable_semantic = self.settings.ENABLE_SEMANTIC and self.search_mode in {
            "semantic",
            "hybrid",
        }
        self.enable_bm25 = self.settings.ENABLE_BM25 and self.search_mode in {
            "bm25",
            "hybrid",
        }
        self.enable_rrf = self.settings.ENABLE_RRF and self.enable_semantic and self.enable_bm25
        self.enable_query_expansion = self.settings.ENABLE_QUERY_EXPANSION
        self.enable_reranker = self.settings.ENABLE_RERANKER
        self.enable_business_ranking = self.settings.ENABLE_BUSINESS_RANKING

        self.qdrant_url = self.settings.qdrant_url
        self.qdrant_api_key = self.settings.QDRANT_API_KEY
        self.collection_name = self.settings.QDRANT_COLLECTION
        self.embedding_model = self.settings.EMBEDDING_MODEL
        self.embedding_device = self.settings.EMBEDDING_DEVICE

        self.qdrant = QdrantCollectionManager(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )

        self.embedder = None
        if self.enable_semantic:
            self.embedder = BGEM3Embedder(
                model_name=self.embedding_model,
                device=self.embedding_device,
            )

        self.registry = KnowledgeRegistry("knowledge/v1")
        self.query_processor = QueryProcessor(self.registry)
        self.query_expander = QueryExpander(self.registry)
        self.filter_builder = MetadataFilterBuilder()

        self.retriever = None
        if self.enable_semantic:
            self.retriever = QdrantRetriever(
                client=self.qdrant.client,
                collection_name=self.collection_name,
            )

        self.bm25 = None
        bm25_index = Path("storage/bm25.pkl")
        if self.enable_bm25:
            if bm25_index.exists():
                self.bm25 = BM25Retriever(str(bm25_index))
            else:
                logger.warning("BM25 enabled but %s was not found; disabling BM25", bm25_index)
                self.enable_bm25 = False
                self.enable_rrf = False

        self.hybrid_retriever = HybridRetriever(
            semantic_retriever=self.retriever,
            bm25_retriever=self.bm25,
        )
        self.rrf = ReciprocalRankFusion(k=60)

        self.reranker = None
        if self.enable_reranker:
            self.reranker = CrossEncoderReranker(self.settings.RERANKER_MODEL)

        self.business_ranker = None
        if self.enable_business_ranking:
            self.business_ranker = BusinessRanker(self.registry)


        logger.info("=" * 70)
        logger.info("Search Engine Configuration")
        logger.info("SEARCH_MODE              : %s", self.settings.SEARCH_MODE)
        logger.info("ENABLE_SEMANTIC          : %s", self.settings.ENABLE_SEMANTIC)
        logger.info("ENABLE_BM25             : %s", self.settings.ENABLE_BM25)
        logger.info("ENABLE_RRF              : %s", self.settings.ENABLE_RRF)
        logger.info("ENABLE_QUERY_EXPANSION  : %s", self.settings.ENABLE_QUERY_EXPANSION)
        logger.info("ENABLE_RERANKER         : %s", self.settings.ENABLE_RERANKER)
        logger.info("ENABLE_BUSINESS_RANKING : %s", self.settings.ENABLE_BUSINESS_RANKING)
        logger.info("=" * 70)

        self.search_service = SearchService(
            query_processor=self.query_processor,
            query_expander=self.query_expander,
            filter_builder=self.filter_builder,
            embedder=self.embedder,
            hybrid_retriever=self.hybrid_retriever,
            rrf=self.rrf,
            reranker=self.reranker,
            business_ranker=self.business_ranker,
            settings=self.settings,
            enable_semantic=self.enable_semantic,
            enable_bm25=self.enable_bm25,
            enable_rrf=self.enable_rrf,
            enable_query_expansion=self.enable_query_expansion,
            enable_business_ranking=self.enable_business_ranking,
        )




        


container = Container()
