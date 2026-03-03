"""Ollama router for @copilot, @lucidia, and @blackboxprogramming mentions.

All requests that mention @copilot, @lucidia, or @blackboxprogramming are
routed directly to the local Ollama instance.  No external AI providers
(ChatGPT, Copilot, Claude, etc.) are contacted.

Example
-------

```python
from native_ai_quantum_energy.ollama_router import dispatch

# All three handles reach the same local Ollama server
response = dispatch("@copilot explain quantum entanglement")
response = dispatch("@lucidia what is a Hadamard gate?")
response = dispatch("@blackboxprogramming optimise this circuit")
```
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Optional


# ── Public constants ──────────────────────────────────────────────────────────

#: Default base URL for the local Ollama service.
OLLAMA_BASE_URL: str = "http://localhost:11434"

#: Default model name used when none is specified by the caller.
DEFAULT_MODEL: str = "llama3"

#: All @handles that are routed to the local Ollama instance.
OLLAMA_HANDLES: frozenset[str] = frozenset(
    {"@copilot", "@lucidia", "@blackboxprogramming"}
)

# ── Internal helpers ──────────────────────────────────────────────────────────

_HANDLE_PATTERN: re.Pattern[str] = re.compile(
    r"@(?:copilot|lucidia|blackboxprogramming)\b", re.IGNORECASE
)


# ── Public API ────────────────────────────────────────────────────────────────


def contains_ollama_handle(text: str) -> bool:
    """Return ``True`` if *text* contains at least one recognised @handle.

    The check is case-insensitive, so ``@Copilot``, ``@LUCIDIA``, and
    ``@BlackBoxProgramming`` are all accepted.

    Parameters
    ----------
    text : str
        Arbitrary user input to inspect.

    Returns
    -------
    bool
        ``True`` when one of the routing handles is present, ``False``
        otherwise.
    """
    return bool(_HANDLE_PATTERN.search(text))


def strip_handles(text: str) -> str:
    """Remove all recognised @handles from *text*.

    The stripped text is returned with surrounding whitespace removed so
    that the prompt sent to Ollama is clean.

    Parameters
    ----------
    text : str
        User input that may contain @handle prefixes.

    Returns
    -------
    str
        The input with every occurrence of the routing handles removed and
        leading/trailing whitespace stripped.
    """
    return _HANDLE_PATTERN.sub("", text).strip()


def route_to_ollama(
    prompt: str,
    model: str = DEFAULT_MODEL,
    base_url: str = OLLAMA_BASE_URL,
) -> str:
    """Send *prompt* to the local Ollama instance and return its response.

    The @handle prefixes are stripped before the prompt is forwarded so
    that Ollama receives a clean query.  All communication goes to the
    local Ollama server; no external AI providers are contacted.

    Parameters
    ----------
    prompt : str
        User prompt (with or without @handle mentions).
    model : str, optional
        Ollama model to query.  Defaults to ``DEFAULT_MODEL``.
    base_url : str, optional
        Base URL of the local Ollama service.  Defaults to
        ``OLLAMA_BASE_URL`` (``http://localhost:11434``).

    Returns
    -------
    str
        The text response returned by Ollama.

    Raises
    ------
    OllamaConnectionError
        If the Ollama service cannot be reached (network error, service
        not running, wrong URL, etc.).
    OllamaRequestError
        If Ollama returns an HTTP error or a response that cannot be
        parsed.
    """
    clean_prompt = strip_handles(prompt)
    url = f"{base_url}/api/generate"
    payload = json.dumps(
        {"model": model, "prompt": clean_prompt, "stream": False}
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise OllamaConnectionError(
            f"Cannot reach Ollama at {base_url}: {exc}"
        ) from exc

    try:
        result = json.loads(body)
        return result["response"]
    except (json.JSONDecodeError, KeyError) as exc:
        raise OllamaRequestError(
            f"Unexpected response from Ollama: {exc}"
        ) from exc


def dispatch(
    prompt: str,
    model: str = DEFAULT_MODEL,
    base_url: str = OLLAMA_BASE_URL,
) -> str:
    """Route *prompt* to Ollama when it contains a recognised @handle.

    This is the primary entry point for the routing layer.  Every prompt
    that mentions ``@copilot``, ``@lucidia``, or ``@blackboxprogramming``
    is forwarded to the local Ollama instance.  No external AI providers
    are used.

    Parameters
    ----------
    prompt : str
        The user prompt, expected to include at least one @handle.
    model : str, optional
        Ollama model name.  Defaults to ``DEFAULT_MODEL``.
    base_url : str, optional
        Ollama server base URL.  Defaults to ``OLLAMA_BASE_URL``.

    Returns
    -------
    str
        The response text from Ollama.

    Raises
    ------
    ValueError
        If the prompt does not contain any of the recognised @handles.
    OllamaConnectionError
        If the local Ollama service cannot be reached.
    OllamaRequestError
        If Ollama returns an unexpected or error response.
    """
    if not contains_ollama_handle(prompt):
        raise ValueError(
            "Prompt must include one of the following handles to be routed "
            "to the local Ollama instance: "
            + ", ".join(sorted(OLLAMA_HANDLES))
        )
    return route_to_ollama(prompt, model=model, base_url=base_url)


# ── Exceptions ────────────────────────────────────────────────────────────────


class OllamaConnectionError(OSError):
    """Raised when the local Ollama service cannot be reached."""


class OllamaRequestError(RuntimeError):
    """Raised when Ollama returns an unexpected or error response."""
