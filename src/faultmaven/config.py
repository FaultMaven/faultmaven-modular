"""
Configuration validation for FaultMaven.

Validates required environment variables on startup to provide clear error messages.
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Ensure .env is loaded before validation
from dotenv import load_dotenv

# Find and load .env file from project root
# This handles cases where the script is run from different directories
project_root = Path(__file__).parent.parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)


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
            "  - gemini\n"
            "  - fireworks\n"
            "  - openrouter\n"
            "  - ollama\n\n"
            "Example:\n"
            "  LLM_PROVIDER=groq\n"
            "  GROQ_API_KEY=gsk_..."
        )

    # Validate provider-specific configuration
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key or api_key.startswith("your-") or api_key == "sk-...":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'openai' but OPENAI_API_KEY is not configured.\n\n"
                "Please add your OpenAI API key to .env:\n"
                "  OPENAI_API_KEY=sk-...\n\n"
                "Get your API key at: https://platform.openai.com/api-keys"
            )

    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not api_key or api_key.startswith("your-") or api_key == "sk-ant-...":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'anthropic' but ANTHROPIC_API_KEY is not configured.\n\n"
                "Please add your Anthropic API key to .env:\n"
                "  ANTHROPIC_API_KEY=sk-ant-...\n\n"
                "Get your API key at: https://console.anthropic.com/"
            )

    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key or api_key == "gsk_...":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'groq' but GROQ_API_KEY is not configured.\n\n"
                "Please add your Groq API key to .env:\n"
                "  GROQ_API_KEY=gsk_...\n\n"
                "Get your API key at: https://console.groq.com/ (FREE tier available!)"
            )

    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "...":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'gemini' but GEMINI_API_KEY is not configured.\n\n"
                "Please add your Gemini API key to .env:\n"
                "  GEMINI_API_KEY=...\n\n"
                "Get your API key at: https://makersuite.google.com/app/apikey"
            )

    elif provider == "fireworks":
        api_key = os.getenv("FIREWORKS_API_KEY", "").strip()
        if not api_key or api_key == "...":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'fireworks' but FIREWORKS_API_KEY is not configured.\n\n"
                "Please add your Fireworks API key to .env:\n"
                "  FIREWORKS_API_KEY=...\n\n"
                "Get your API key at: https://fireworks.ai/api-keys"
            )

    elif provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        if not api_key or api_key == "sk-or-...":
            raise ConfigurationError(
                "LLM_PROVIDER is set to 'openrouter' but OPENROUTER_API_KEY is not configured.\n\n"
                "Please add your OpenRouter API key to .env:\n"
                "  OPENROUTER_API_KEY=sk-or-...\n\n"
                "Get your API key at: https://openrouter.ai/keys"
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
            "  - gemini\n"
            "  - fireworks\n"
            "  - openrouter\n"
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
