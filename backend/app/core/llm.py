"""OpenAI-compatible abstraction designed for pluggable providers."""

from dataclasses import dataclass


@dataclass
class LLMRequest:
    """Standardized request payload for a provider adapter."""

    system_prompt: str
    user_prompt: str
    temperature: float


@dataclass
class LLMResponse:
    """Standardized response payload for deterministic post-processing."""

    content: str
    model: str
    latency_ms: int


class OpenAICompatibleProvider:
    """Provider contract for OpenAI-style chat completion interfaces."""

    def generate(self, request: LLMRequest) -> LLMResponse:
        """Placeholder generate method for future concrete adapter."""
        return LLMResponse(content="{}", model="stub-model", latency_ms=0)
