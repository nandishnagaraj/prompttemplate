from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from langchain_openai import AzureChatOpenAI, ChatOpenAI


@dataclass
class LLMConfig:
    provider: str  # "openai" | "azure" | "mock"
    model_name: str = "gpt-4.1-mini"
    azure_endpoint: Optional[str] = None
    azure_deployment: Optional[str] = None


class MockLLM:
    """Deterministic fallback for wiring/testing without keys."""

    def invoke(self, prompt: str) -> str:
        # Keep it deterministic and short; return a structured placeholder.
        return (
            "[MOCK OUTPUT]\n\n"
            "This is a deterministic mock response.\n"
            "Prompt hash: " + str(abs(hash(prompt)) % 10_000_000)
        )


class _LangChainTextAdapter:
    """Normalize LangChain chat model outputs to plain text for existing nodes."""

    def __init__(self, model: Any) -> None:
        self._model = model

    def invoke(self, prompt: str) -> str:
        result = self._model.invoke(prompt)
        if isinstance(result, str):
            return result
        content = getattr(result, "content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(str(item))
            return "\n".join(p for p in parts if p)
        return str(result)


def build_llm() -> object:
    """Return an object with .invoke(str)->str."""
    openai_key = os.getenv("OPENAI_API_KEY")
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

    if azure_key and azure_endpoint and azure_deployment:
        model = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            openai_api_key=azure_key,
            openai_api_version=azure_api_version,
            temperature=0,
        )
        return _LangChainTextAdapter(model)

    if openai_key:
        model_name = os.getenv("MODEL_NAME", "gpt-4.1-mini")
        model = ChatOpenAI(model=model_name, api_key=openai_key, temperature=0)
        return _LangChainTextAdapter(model)

    return MockLLM()
