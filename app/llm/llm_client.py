"""
LLM Client

Provider-agnostic LLM interface.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from .models import LLMResponse

logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    """
    Base class for all LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        raise NotImplementedError


# ---------------------------------------------------------
# Gemini
# ---------------------------------------------------------


class GeminiClient(BaseLLMClient):

    def __init__(
        self,
        model,
    ):
        self.model = model

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:

        prompt = f"{system_prompt}\n\n{user_prompt}"

        response = self.model.generate_content(prompt)

        return LLMResponse(
            answer=response.text,
            provider="gemini",
            model=getattr(self.model, "model_name", "gemini"),
        )


# ---------------------------------------------------------
# OpenAI
# ---------------------------------------------------------


class OpenAIClient(BaseLLMClient):

    def __init__(
        self,
        client,
        model: str,
    ):
        self.client = client
        self.model = model

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        message = response.choices[0].message.content

        usage = getattr(response, "usage", None)

        return LLMResponse(

            answer=message,

            provider="openai",

            model=self.model,

            prompt_tokens=getattr(
                usage,
                "prompt_tokens",
                0,
            ),

            completion_tokens=getattr(
                usage,
                "completion_tokens",
                0,
            ),

            total_tokens=getattr(
                usage,
                "total_tokens",
                0,
            ),
        )


# ---------------------------------------------------------
# Ollama
# ---------------------------------------------------------


class OllamaClient(BaseLLMClient):

    def __init__(
        self,
        client,
        model: str,
    ):
        self.client = client
        self.model = model

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:

        response = self.client.chat(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return LLMResponse(

            answer=response["message"]["content"],

            provider="ollama",

            model=self.model,
        )


# ---------------------------------------------------------
# Factory
# ---------------------------------------------------------


class LLMClientFactory:
    """
    Factory for creating provider-specific clients.
    """

    @staticmethod
    def create(
        *,
        provider: str,
        client,
        model: str,
    ) -> BaseLLMClient:

        provider = provider.lower()

        if provider == "gemini":
            return GeminiClient(client)

        if provider == "openai":
            return OpenAIClient(client, model)

        if provider == "ollama":
            return OllamaClient(client, model)

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )