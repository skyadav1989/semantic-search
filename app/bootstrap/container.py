"""
Application Dependency Container

Creates singleton instances used by the API.
"""

from __future__ import annotations
from huggingface_hub.inference._generated.types import zero_shot_image_classification
import logging
import google.generativeai as genai
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
from app.facets.facet_service import FacetService
from app.recommendation.query_builder import RecommendationQueryBuilder
from app.recommendation.business_rules import BusinessRuleEngine
from app.recommendation.strategy import RecommendationStrategy
from app.recommendation.similarity import SimilarityEngine
from app.recommendation.recommendation_service import RecommendationService
from app.llm.context_builder import ContextBuilder
from app.llm.citations import CitationBuilder
from app.llm.response_formatter import ResponseFormatter
from app.llm.answer_generator import AnswerGenerator
from app.chat.memory import ConversationMemory
from app.chat.conversation import ConversationManager
from app.chat.followup_detector import FollowupDetector
from app.chat.context_manager import ContextManager
from app.chat.prompt_builder import PromptBuilder
from app.chat.chat_service import ChatService
from app.chat.response_postprocessor import ResponsePostProcessor

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
        

        # LLM Components
        self.context_builder = ContextBuilder()

        self.citation_builder = CitationBuilder()

        self.response_formatter = ResponseFormatter()

        
        
        self.facet_service = None
        if getattr(self.settings, "ENABLE_FACETS", True):
            self.facet_service = FacetService()

        #
        # LLM
        #
        self.llm_client = None
        self.answer_generator = None

        if self.settings.ENABLE_LLM:

            if self.settings.LLM_PROVIDER.lower() == "gemini":

                print('KEY '+self.settings.GEMINI_API_KEY)

                genai.configure(
                    api_key=self.settings.GEMINI_API_KEY,
                )

                model = genai.GenerativeModel(
                    self.settings.LLM_MODEL,
                )

                from app.llm.llm_client import GeminiClient

                self.llm_client = GeminiClient(model)

                self.answer_generator = AnswerGenerator(
                    llm_client=self.llm_client,
                    context_builder=self.context_builder,
                )

                logger.info(
                    "Gemini initialized (%s)",
                    self.settings.LLM_MODEL,
                )
        #
        # Recommendation Engine
        #
        self.recommendation_query_builder = RecommendationQueryBuilder()

        self.recommendation_business_rules = BusinessRuleEngine()

        self.recommendation_strategy = RecommendationStrategy()

        self.recommendation_similarity = SimilarityEngine()

        self.recommendation_service = RecommendationService(
            retriever=self.retriever,
            filter_builder=self.filter_builder,
            query_builder=self.recommendation_query_builder,
            business_rules=self.recommendation_business_rules,
            strategy=self.recommendation_strategy,
            similarity=self.recommendation_similarity,
        )
        


        logger.info("=" * 70)
        logger.info("Search Engine Configuration")
        logger.info("SEARCH_MODE              : %s", self.settings.SEARCH_MODE)
        logger.info("ENABLE_SEMANTIC          : %s", self.settings.ENABLE_SEMANTIC)
        logger.info("ENABLE_BM25             : %s", self.settings.ENABLE_BM25)
        logger.info("ENABLE_RRF              : %s", self.settings.ENABLE_RRF)
        logger.info("ENABLE_QUERY_EXPANSION  : %s", self.settings.ENABLE_QUERY_EXPANSION)
        logger.info("ENABLE_RERANKER         : %s", self.settings.ENABLE_RERANKER)
        logger.info("ENABLE_BUSINESS_RANKING : %s", self.settings.ENABLE_BUSINESS_RANKING)
        logger.info(
            "ENABLE_FACETS           : %s",
            getattr(self.settings, "ENABLE_FACETS", True),
        )

        logger.info(
            "RECOMMENDATION_ENGINE   : ENABLED"
        )
        logger.info(
            "ENABLE_LLM              : %s",
            getattr(self.settings, "ENABLE_LLM", False),
        )

        logger.info(
            "LLM Provider : %s",
            self.settings.LLM_PROVIDER,
        )

        logger.info(
            "LLM Model : %s",
            self.settings.LLM_MODEL,
        )
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
            facet_service=self.facet_service,
            answer_generator=self.answer_generator,
            settings=self.settings,
            enable_semantic=self.enable_semantic,
            enable_bm25=self.enable_bm25,
            enable_rrf=self.enable_rrf,
            enable_query_expansion=self.enable_query_expansion,
            enable_business_ranking=self.enable_business_ranking,
        )


        #
        # Chat Components
        #

        self.chat_memory = ConversationMemory()

        self.chat_conversation = ConversationManager()

        self.chat_followup = FollowupDetector()

        self.chat_context = ContextManager()

        self.chat_prompt_builder = PromptBuilder()

        self.chat_postprocessor = ResponsePostProcessor()

        self.chat_service = ChatService(
            memory=self.chat_memory,
            conversation=self.chat_conversation,
            followup_detector=self.chat_followup,
            context_manager=self.chat_context,
            prompt_builder=self.chat_prompt_builder,
            response_postprocessor=self.chat_postprocessor,
            search_service=self.search_service,
            answer_generator=self.answer_generator,
        )




        


container = Container()
