"""Tests for the Ollama router module.

These tests verify routing behaviour without requiring a live Ollama
instance.  All network calls are intercepted by monkeypatching
``urllib.request.urlopen``.
"""

from __future__ import annotations

import io
import json
import urllib.error
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from native_ai_quantum_energy.ollama_router import (
    DEFAULT_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_HANDLES,
    OllamaConnectionError,
    OllamaRequestError,
    contains_ollama_handle,
    dispatch,
    route_to_ollama,
    strip_handles,
)


# ── Helper ────────────────────────────────────────────────────────────────────


def _mock_urlopen(response_text: str) -> Any:
    """Return a context-manager mock that yields an HTTP-like response."""
    body = json.dumps({"response": response_text}).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.read.return_value = body
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


# ── contains_ollama_handle ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "text",
    [
        "@copilot explain this",
        "@lucidia what is entropy?",
        "@blackboxprogramming optimise the circuit",
        "Hi @Copilot, please help",          # mixed case
        "question for @LUCIDIA here",        # upper case
        "@BlackBoxProgramming do something", # camel case
        "use @copilot and @lucidia together",# multiple handles
    ],
)
def test_contains_handle_returns_true(text: str) -> None:
    assert contains_ollama_handle(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "just a plain question",
        "@chatgpt help me",
        "@claude answer this",
        "@openai response please",
        "no handle at all",
    ],
)
def test_contains_handle_returns_false(text: str) -> None:
    assert contains_ollama_handle(text) is False


# ── strip_handles ─────────────────────────────────────────────────────────────


def test_strip_handles_removes_copilot() -> None:
    assert strip_handles("@copilot explain this") == "explain this"


def test_strip_handles_removes_lucidia() -> None:
    assert strip_handles("@lucidia what is entropy?") == "what is entropy?"


def test_strip_handles_removes_blackboxprogramming() -> None:
    assert strip_handles("@blackboxprogramming run a sim") == "run a sim"


def test_strip_handles_case_insensitive() -> None:
    assert strip_handles("@COPILOT help") == "help"
    assert strip_handles("@Lucidia help") == "help"
    assert strip_handles("@BlackBoxProgramming help") == "help"


def test_strip_handles_removes_multiple() -> None:
    result = strip_handles("@copilot and @lucidia and @blackboxprogramming: hi")
    assert "@copilot" not in result.lower()
    assert "@lucidia" not in result.lower()
    assert "@blackboxprogramming" not in result.lower()


def test_strip_handles_leaves_unrelated_text() -> None:
    result = strip_handles("@copilot tell me about quantum gates")
    assert "quantum gates" in result


# ── route_to_ollama ───────────────────────────────────────────────────────────


def test_route_to_ollama_sends_correct_payload() -> None:
    mock_resp = _mock_urlopen("hello from ollama")
    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
        result = route_to_ollama("explain superposition", model="llama3")

    assert result == "hello from ollama"
    # Inspect the Request that was passed to urlopen
    call_args = mock_open.call_args[0][0]
    sent_payload = json.loads(call_args.data.decode("utf-8"))
    assert sent_payload["model"] == "llama3"
    assert sent_payload["prompt"] == "explain superposition"
    assert sent_payload["stream"] is False


def test_route_to_ollama_strips_handles_before_forwarding() -> None:
    mock_resp = _mock_urlopen("answer")
    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
        route_to_ollama("@copilot explain entanglement")

    call_args = mock_open.call_args[0][0]
    sent_payload = json.loads(call_args.data.decode("utf-8"))
    assert "@copilot" not in sent_payload["prompt"]
    assert "explain entanglement" in sent_payload["prompt"]


def test_route_to_ollama_uses_custom_base_url() -> None:
    custom_url = "http://my-server:11434"
    mock_resp = _mock_urlopen("ok")
    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
        route_to_ollama("hello", base_url=custom_url)

    call_args = mock_open.call_args[0][0]
    assert call_args.full_url.startswith(custom_url)


def test_route_to_ollama_raises_connection_error_on_network_failure() -> None:
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("connection refused"),
    ):
        with pytest.raises(OllamaConnectionError, match="Cannot reach Ollama"):
            route_to_ollama("hello")


def test_route_to_ollama_raises_request_error_on_bad_json() -> None:
    bad_resp = MagicMock()
    bad_resp.read.return_value = b"not-json"
    bad_resp.__enter__ = lambda s: s
    bad_resp.__exit__ = MagicMock(return_value=False)
    with patch("urllib.request.urlopen", return_value=bad_resp):
        with pytest.raises(OllamaRequestError, match="Unexpected response"):
            route_to_ollama("hello")


def test_route_to_ollama_raises_request_error_on_missing_key() -> None:
    bad_resp = MagicMock()
    bad_resp.read.return_value = json.dumps({"model": "llama3"}).encode()
    bad_resp.__enter__ = lambda s: s
    bad_resp.__exit__ = MagicMock(return_value=False)
    with patch("urllib.request.urlopen", return_value=bad_resp):
        with pytest.raises(OllamaRequestError, match="Unexpected response"):
            route_to_ollama("hello")


# ── dispatch ──────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "handle",
    ["@copilot", "@lucidia", "@blackboxprogramming"],
)
def test_dispatch_routes_all_handles_to_ollama(handle: str) -> None:
    mock_resp = _mock_urlopen(f"response for {handle}")
    with patch("urllib.request.urlopen", return_value=mock_resp):
        result = dispatch(f"{handle} what is quantum computing?")
    assert "response for" in result


def test_dispatch_raises_value_error_without_handle() -> None:
    with pytest.raises(ValueError, match="@copilot"):
        dispatch("plain question without any handle")


def test_dispatch_does_not_contact_external_providers() -> None:
    """Verify that dispatch only ever calls the specified local Ollama URL."""
    expected_base = "http://localhost:11434"
    mock_resp = _mock_urlopen("ok")
    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
        dispatch("@copilot hello", base_url=expected_base)

    for call in mock_open.call_args_list:
        req = call[0][0]
        assert req.full_url.startswith(expected_base), (
            "dispatch must only contact the local Ollama instance"
        )


def test_dispatch_accepts_custom_model_and_url() -> None:
    mock_resp = _mock_urlopen("custom")
    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
        result = dispatch(
            "@lucidia summarise this",
            model="mistral",
            base_url="http://127.0.0.1:11434",
        )
    assert result == "custom"
    call_args = mock_open.call_args[0][0]
    sent_payload = json.loads(call_args.data.decode("utf-8"))
    assert sent_payload["model"] == "mistral"


# ── OLLAMA_HANDLES constant ───────────────────────────────────────────────────


def test_ollama_handles_contains_required_handles() -> None:
    assert "@copilot" in OLLAMA_HANDLES
    assert "@lucidia" in OLLAMA_HANDLES
    assert "@blackboxprogramming" in OLLAMA_HANDLES


def test_ollama_handles_does_not_include_external_providers() -> None:
    for handle in OLLAMA_HANDLES:
        assert "openai" not in handle
        assert "claude" not in handle
        assert "chatgpt" not in handle
