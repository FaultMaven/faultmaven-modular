"""
Configuration validation for FaultMaven.

Validates required environment variables on startup to provide clear error messages.
"""

import os
import sys
from typing import Optional


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""
    pass


def validate_llm_configuration() -> None:
    """
    Validate LLM provider configuration.

    Raises:
        ConfigurationError: If LLM provider is not configured properly
    """
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()

    if not provider:
        raise ConfigurationError(
            "LLM_PROVIDER is not configured.\n\n"
            "Please set LLM_PROVIDER in your .env file to one of:\n"
            "  - openai\n"
            "  - anthropic\n"
            "  - groq\n"
            "  - ollama\n\n"
            "Example:\n"
            "  LLM_PROVIDER=openai\n"
            "  OPENAI_API_KEY=sk-..."
        )

    # Validate provider-specific configuration
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key or api_key == "your-openai-api-key-here":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'openai' but OPENAI_API_KEY is not configured.\n\n"
                "Please add your OpenAI API key to .env:\n"
                "  OPENAI_API_KEY=sk-...\n\n"
                "Get your API key at: https://platform.openai.com/api-keys"
            )

    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not api_key or api_key == "your-anthropic-api-key-here":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'anthropic' but ANTHROPIC_API_KEY is not configured.\n\n"
                "Please add your Anthropic API key to .env:\n"
                "  ANTHROPIC_API_KEY=sk-ant-...\n\n"
                "Get your API key at: https://console.anthropic.com/"
            )

    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key:
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'groq' but GROQ_API_KEY is not configured.\n\n"
                "Please add your Groq API key to .env:\n"
                "  GROQ_API_KEY=gsk_...\n\n"
                "Get your API key at: https://console.groq.com/ (FREE tier available!)"
            )

    elif provider == "ollama":
        ollama_host = os.getenv("OLLAMA_HOST", "").strip()
        if not ollama_host:
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'ollama' but OLLAMA_HOST is not configured.\n\n"
                "Please configure Ollama in .env:\n"
                "  OLLAMA_HOST=http://localhost:11434\n"
                "  OLLAMA_MODEL=llama3.2\n\n"
                "Install Ollama: https://ollama.ai/"
            )

    else:
        raise ConfigurationError(
            f"Invalid LLM_PROVIDER: '{provider}'\n\n"
            "Supported providers:\n"
            "  - openai\n"
            "  - anthropic\n"
            "  - groq\n"
            "  - ollama\n\n"
            "Please update your .env file."
        )


def validate_network_configuration() -> None:
    """
    Validate network configuration for remote access.

    This is a warning, not an error - localhost is valid for local development.
    """
    server_host = os.getenv("SERVER_HOST", "localhost").strip()

    # Just log a warning if using localhost - it's valid for local dev
    if server_host == "localhost":
        # This is fine for local development
        pass


def validate_required_configuration() -> None:
    """
    Validate all required configuration on startup.

    Raises:
        ConfigurationError: If any required configuration is missing or invalid
    """
    try:
        # Validate LLM configuration (required)
        validate_llm_configuration()

        # Validate network configuration (warning only)
        validate_network_configuration()

    except ConfigurationError as e:
        # Print a clear error message
        print("\n" + "=" * 80, file=sys.stderr)
        print("❌ CONFIGURATION ERROR", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print(f"\n{str(e)}\n", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print("\nPlease fix the configuration and restart FaultMaven.\n", file=sys.stderr)

        # Re-raise to stop startup
        raise


def get_env_or_fail(key: str, description: str) -> str:
    """
    Get an environment variable or fail with a clear error message.

    Args:
        key: Environment variable name
        description: Human-readable description of the variable

    Returns:
        The environment variable value

    Raises:
        ConfigurationError: If the variable is not set
    """
    value = os.getenv(key, "").strip()
    if not value:
        raise ConfigurationError(
            f"{key} is not configured.\n\n"
            f"Please set {key} in your .env file.\n"
            f"Description: {description}"
        )
    return value
