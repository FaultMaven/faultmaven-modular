"""
Provider factory functions for FaultMaven.

Creates provider instances based on environment configuration.
"""

import os
from typing import Optional
from faultmaven.providers.interfaces import LLMProvider
from faultmaven.providers.llm.openai import OpenAIProvider
from faultmaven.providers.llm.anthropic import AnthropicProvider
from faultmaven.providers.llm.ollama import OllamaProvider


def create_llm_provider() -> LLMProvider:
    """
    Create LLM provider based on LLM_PROVIDER environment variable.

    Supported providers:
    - openai: OpenAI GPT models
    - anthropic: Anthropic Claude models
    - groq: Groq (uses OpenAI-compatible API)
    - ollama: Local Ollama models
    - gemini: Google Gemini (uses OpenAI-compatible API via base_url)
    - fireworks: Fireworks AI (uses OpenAI-compatible API)
    - openrouter: OpenRouter (uses OpenAI-compatible API)

    Returns:
        LLMProvider instance configured for the selected provider

    Raises:
        ValueError: If LLM_PROVIDER is not set or provider is not supported
    """
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()

    if not provider:
        raise ValueError(
            "LLM_PROVIDER environment variable is not set. "
            "Please set it in your .env file."
        )

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider")

        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        organization = os.getenv("OPENAI_ORGANIZATION")

        return OpenAIProvider(
            api_key=api_key,
            default_model=model,
            organization=organization,
        )

    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider")

        model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

        return AnthropicProvider(
            api_key=api_key,
            default_model=model,
        )

    elif provider == "groq":
        # Groq uses OpenAI-compatible API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is required for Groq provider")

        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

        # Use OpenAI provider with Groq base URL
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        # Create a custom provider wrapper
        provider_instance = OpenAIProvider(
            api_key=api_key,
            default_model=model,
        )
        # Override client with Groq endpoint
        provider_instance.client = client

        return provider_instance

    elif provider == "gemini":
        # Gemini can use OpenAI-compatible API via base_url
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini provider")

        model = os.getenv("GEMINI_MODEL", "gemini-pro")
        base_url = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")

        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        provider_instance = OpenAIProvider(
            api_key=api_key,
            default_model=model,
        )
        provider_instance.client = client

        return provider_instance

    elif provider == "fireworks":
        # Fireworks uses OpenAI-compatible API
        api_key = os.getenv("FIREWORKS_API_KEY")
        if not api_key:
            raise ValueError("FIREWORKS_API_KEY is required for Fireworks provider")

        model = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/llama-v3p1-70b-instruct")

        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.fireworks.ai/inference/v1",
        )

        provider_instance = OpenAIProvider(
            api_key=api_key,
            default_model=model,
        )
        provider_instance.client = client

        return provider_instance

    elif provider == "openrouter":
        # OpenRouter uses OpenAI-compatible API
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is required for OpenRouter provider")

        model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-sonnet")

        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        provider_instance = OpenAIProvider(
            api_key=api_key,
            default_model=model,
        )
        provider_instance.client = client

        return provider_instance

    elif provider == "ollama":
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.2")

        return OllamaProvider(
            host=host,
            default_model=model,
        )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: '{provider}'. "
            f"Supported providers: openai, anthropic, groq, gemini, fireworks, openrouter, ollama"
        )
