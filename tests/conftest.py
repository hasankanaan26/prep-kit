"""Offline tests for the prep-kit scripts. No network, no keys, no money.

Run from prep-kit/:  pytest
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))

KEY_VARS = ["GEMINI_API_KEY", "GEMINI_MODEL", "GEMINI_BASE_URL",
            "OPENROUTER_API_KEY", "OPENROUTER_MODEL", "OPENROUTER_BASE_URL",
            "OLLAMA_MODEL", "OLLAMA_BASE_URL"]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Whatever is in your own prep-kit/.env must not change the test results."""
    for var in KEY_VARS:
        monkeypatch.delenv(var, raising=False)
