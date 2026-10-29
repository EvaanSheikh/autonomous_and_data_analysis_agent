import pytest

from app.agents.llm_planner import create_llm_planner


def test_llm_planner_requires_supported_provider(monkeypatch):
    monkeypatch.setenv(
        "LLM_PROVIDER",
        "invalid_provider",
    )

    with pytest.raises(ValueError):
        create_llm_planner()


def test_llm_planner_accepts_openrouter(monkeypatch):
    monkeypatch.setenv(
        "LLM_PROVIDER",
        "openrouter",
    )

    assert create_llm_planner() == "openrouter"


def test_llm_planner_accepts_gemini(monkeypatch):
    monkeypatch.setenv(
        "LLM_PROVIDER",
        "gemini",
    )

    assert create_llm_planner() == "gemini"