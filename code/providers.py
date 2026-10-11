"""Three LLM providers, one SDK.

Gemini, OpenRouter and Ollama all speak the same "OpenAI-compatible" API. So
the `openai` Python package can talk to every one of them. The only things
that change are the address (base_url), the key, and the model name.

That is the whole idea of this file: a provider is a URL plus a key.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

KIT_DIR = Path(__file__).resolve().parent.parent  # prep-kit/, wherever you put it
DATA_DIR = KIT_DIR / "data"                       # the kit's own copy of the Nimbus tickets

# The kit has its own .env (prep-kit/.env). It never reads the course's .env.
load_dotenv(KIT_DIR / ".env")


@dataclass(frozen=True)
class Provider:
    name: str
    base_url_env: str
    default_base_url: str
    key_env: str | None   # None means "no key needed" (Ollama runs on your laptop)
    model_env: str
    default_model: str
    get_key_at: str


PROVIDERS: dict[str, Provider] = {
    "gemini": Provider(
        name="gemini",
        base_url_env="GEMINI_BASE_URL",
        default_base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        key_env="GEMINI_API_KEY",
        model_env="GEMINI_MODEL",
        default_model="gemini-3.5-flash-lite",
        get_key_at="https://aistudio.google.com/apikey",
    ),
    "openrouter": Provider(
        name="openrouter",
        base_url_env="OPENROUTER_BASE_URL",
        default_base_url="https://openrouter.ai/api/v1",
        key_env="OPENROUTER_API_KEY",
        model_env="OPENROUTER_MODEL",
        default_model="openrouter/free",
        get_key_at="https://openrouter.ai/settings/keys",
    ),
    "ollama": Provider(
        name="ollama",
        base_url_env="OLLAMA_BASE_URL",
        default_base_url="http://localhost:11434/v1",
        key_env=None,
        model_env="OLLAMA_MODEL",
        default_model="llama3.2",
        get_key_at="https://ollama.com/download (no key: it runs on your machine)",
    ),
}


class SetupError(Exception):
    """Something in your setup is missing. The message says how to fix it."""


def get_provider(name: str) -> Provider:
    try:
        return PROVIDERS[name.lower()]
    except KeyError:
        raise SetupError(
            f"Unknown provider {name!r}. Pick one of: {', '.join(PROVIDERS)}"
        ) from None


def base_url_for(p: Provider) -> str:
    return os.getenv(p.base_url_env) or p.default_base_url


def model_for(p: Provider) -> str:
    return os.getenv(p.model_env) or p.default_model


def key_for(p: Provider) -> str:
    """The API key, or a placeholder for Ollama (the SDK insists on *some* key)."""
    if p.key_env is None:
        return "ollama"
    key = os.getenv(p.key_env, "").strip()
    if not key:
        raise SetupError(
            f"{p.key_env} is not set.\n"
            f"  1. Get a key at {p.get_key_at}\n"
            f"  2. Put it in prep-kit/.env as {p.key_env}=...\n"
            f"  (Module 04 walks through this.)"
        )
    return key


def is_configured(p: Provider) -> bool:
    """True if we have what we need to *try* this provider (says nothing about it working)."""
    return p.key_env is None or bool(os.getenv(p.key_env, "").strip())


def make_client(name: str):
    """An OpenAI SDK client pointed at the provider you asked for."""
    from openai import OpenAI  # imported here so the tests can run without a network

    p = get_provider(name)
    return OpenAI(base_url=base_url_for(p), api_key=key_for(p), timeout=60, max_retries=1)


def explain_error(provider: str, err: Exception) -> str:
    """Turn the usual first-week errors into a sentence with a fix."""
    text = str(err)
    kind = type(err).__name__
    if kind == "APIConnectionError" and provider == "ollama":
        return "Can't reach Ollama. Is it running? Open the Ollama app, or run: ollama serve"
    if kind == "InternalServerError" and provider == "ollama":
        return ("Ollama crashed while loading the model (500). This is usually the graphics card "
                "driver. Quit Ollama, then start it on the CPU only: in PowerShell "
                "$env:CUDA_VISIBLE_DEVICES='-1'; ollama serve  (see module 05).")
    if kind == "APIConnectionError":
        return "Can't reach the provider. Check your internet connection (or a VPN/proxy)."
    if kind == "AuthenticationError" or "401" in text:
        return "The provider rejected your key (401). Copy it again, with no spaces or quotes."
    if kind == "RateLimitError" or "429" in text:
        return ("Rate limited (429): free tiers allow only a few requests per minute or day. "
                "Wait a minute and try again.")
    if kind == "NotFoundError" or "404" in text:
        if provider == "ollama":
            return ("Model not found (404). Download it first: "
                    f"ollama pull {model_for(PROVIDERS['ollama'])}")
        return "Model not found (404). Check the model name in prep-kit/.env."
    return f"{kind}: {text}"
