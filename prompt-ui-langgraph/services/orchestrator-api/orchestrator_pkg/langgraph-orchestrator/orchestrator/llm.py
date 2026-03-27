from __future__ import annotations

import os
import json
from dataclasses import dataclass, field
from typing import Any, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI, ChatOpenAI


@dataclass
class LLMConfig:
    provider: str  # "openai" | "azure" | "gemini" | "mock"
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


class TokenTrackingWrapper:
    """Wraps an LLM to track token usage and costs."""
    
    # Token pricing per 1M tokens (2024 rates)
    PRICING = {
        "gpt-4-1-mini": {"input": 0.15, "output": 0.60},
        "gpt-4": {"input": 3.00, "output": 6.00},
        "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
        "azure": {"input": 0.15, "output": 0.60},  # Azure pricing
    }
    
    def __init__(self, llm: Any, model_name: str = "gpt-4-1-mini"):
        self._llm = llm
        self._model_name = model_name.lower()
        self.token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0.0,
        }
        self._call_count = 0
    
    def invoke(self, prompt: str) -> str:
        result = self._llm.invoke(prompt)
        self._call_count += 1
        
        # Estimate tokens (rough approximation: ~4 chars per token)
        prompt_tokens = len(prompt) // 4
        completion_tokens = len(result) // 4
        
        self.token_usage["prompt_tokens"] += prompt_tokens
        self.token_usage["completion_tokens"] += completion_tokens
        self.token_usage["total_tokens"] += prompt_tokens + completion_tokens
        
        # Calculate cost
        pricing = self._get_pricing()
        prompt_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        completion_cost = (completion_tokens / 1_000_000) * pricing["output"]
        self.token_usage["estimated_cost_usd"] += prompt_cost + completion_cost
        
        return result
    
    def _get_pricing(self) -> dict:
        """Get pricing for the current model."""
        for model_key, pricing in self.PRICING.items():
            if model_key in self._model_name:
                return pricing
        return self.PRICING["gpt-4-1-mini"]  # Default
    
    def reset_metrics(self):
        """Reset token counters."""
        self.token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0.0,
        }
        self._call_count = 0


def build_llm(provider: Optional[str] = None, model_name: Optional[str] = None) -> TokenTrackingWrapper:
    """Return a TokenTrackingWrapper around an LLM with .invoke(str)->str."""
    selected_provider = (provider or os.getenv("LLM_PROVIDER", "auto")).strip().lower()

    openai_key = os.getenv("OPENAI_API_KEY")
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    gemini_key = os.getenv("GEMINI_API_KEY")

    chosen_model = model_name
    base_llm = None

    if selected_provider == "azure":
        if not (azure_key and azure_endpoint and azure_deployment):
            raise ValueError(
                "Azure provider selected but required env vars are missing: "
                "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT"
            )
        chosen_model = chosen_model or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        model = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            openai_api_key=azure_key,
            openai_api_version=azure_api_version,
            temperature=0,
            max_tokens=4096,
        )
        base_llm = _LangChainTextAdapter(model)

    elif selected_provider == "openai":
        if not openai_key:
            raise ValueError("OpenAI provider selected but OPENAI_API_KEY is missing")
        chosen_model = chosen_model or os.getenv("MODEL_NAME", "gpt-4-1-mini")
        model = ChatOpenAI(model=chosen_model, api_key=openai_key, temperature=0, max_tokens=4096)
        base_llm = _LangChainTextAdapter(model)

    elif selected_provider == "gemini":
        if not gemini_key:
            raise ValueError("Gemini provider selected but GEMINI_API_KEY is missing")
        chosen_model = chosen_model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        model = ChatGoogleGenerativeAI(
            model=chosen_model,
            google_api_key=gemini_key,
            temperature=0,
            max_output_tokens=8192,
        )
        base_llm = _LangChainTextAdapter(model)

    elif selected_provider not in {"auto", ""}:
        raise ValueError(f"Unsupported LLM provider: {selected_provider}")

    # Auto-fallback logic
    if base_llm is None:
        if azure_key and azure_endpoint and azure_deployment:
            chosen_model = chosen_model or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
            model = AzureChatOpenAI(
                azure_endpoint=azure_endpoint,
                azure_deployment=azure_deployment,
                openai_api_key=azure_key,
                openai_api_version=azure_api_version,
                temperature=0,
                max_tokens=4096,
            )
            base_llm = _LangChainTextAdapter(model)

        elif openai_key:
            chosen_model = chosen_model or os.getenv("MODEL_NAME", "gpt-4-1-mini")
            model = ChatOpenAI(model=chosen_model, api_key=openai_key, temperature=0, max_tokens=4096)
            base_llm = _LangChainTextAdapter(model)

        elif gemini_key:
            chosen_model = chosen_model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            model = ChatGoogleGenerativeAI(
                model=chosen_model,
                google_api_key=gemini_key,
                temperature=0,
                max_output_tokens=8192,
            )
            base_llm = _LangChainTextAdapter(model)

        else:
            base_llm = MockLLM()

    chosen_model = chosen_model or "gpt-4-1-mini"
    return TokenTrackingWrapper(base_llm, model_name=chosen_model)
