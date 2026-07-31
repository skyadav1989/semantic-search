"""
LLM Module Constants
"""

from __future__ import annotations

#
# Supported Providers
#
OPENAI = "openai"
GEMINI = "gemini"
OLLAMA = "ollama"
OPENROUTER = "openrouter"
LM_STUDIO = "lmstudio"

SUPPORTED_PROVIDERS = (
    OPENAI,
    GEMINI,
    OLLAMA,
    OPENROUTER,
    LM_STUDIO,
)

#
# Prompt Types
#
SEARCH_PROMPT = "search"
COMPARE_PROMPT = "compare"
RECOMMENDATION_PROMPT = "recommendation"
EXPLANATION_PROMPT = "explanation"

#
# Default Models
#
DEFAULT_OPENAI_MODEL = "gpt-5"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
DEFAULT_OPENROUTER_MODEL = "openai/gpt-5"
DEFAULT_LM_STUDIO_MODEL = "local-model"

#
# Generation Settings
#
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOP_P = 0.9
DEFAULT_MAX_TOKENS = 1024

#
# Context Settings
#
MAX_PRODUCTS_IN_CONTEXT = 10
MAX_CONTEXT_CHARACTERS = 15000

#
# Citation Settings
#
ENABLE_CITATIONS = True
ENABLE_PRODUCT_LINKS = True

#
# Conversation Memory
#
MAX_CHAT_HISTORY = 10

#
# Safety
#
SYSTEM_ROLE = "system"
USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"

#
# Response Format
#
RESPONSE_FORMAT_TEXT = "text"
RESPONSE_FORMAT_MARKDOWN = "markdown"
RESPONSE_FORMAT_JSON = "json"

SUPPORTED_RESPONSE_FORMATS = (
    RESPONSE_FORMAT_TEXT,
    RESPONSE_FORMAT_MARKDOWN,
    RESPONSE_FORMAT_JSON,
)