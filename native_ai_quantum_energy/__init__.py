"""Top‑level package for Native AI Quantum Energy Lab.

This package exposes the core simulation classes for quantum circuits and
energy/particle dynamics.  Importing from the package will pull in
`QuantumCircuit` and the energy‑simulation functions directly.

It also exposes the Ollama routing layer, which directs every request
mentioning @copilot, @lucidia, or @blackboxprogramming to the local
Ollama instance without contacting any external AI providers.
"""

from .quantum_simulator import QuantumCircuit
from .energy_simulator import (
    solar_panel_output,
    battery_discharge,
    simulate_particle_collision,
)
from .ollama_router import (
    dispatch,
    route_to_ollama,
    contains_ollama_handle,
    strip_handles,
    OLLAMA_BASE_URL,
    DEFAULT_MODEL,
    OLLAMA_HANDLES,
    OllamaConnectionError,
    OllamaRequestError,
)

__all__ = [
    "QuantumCircuit",
    "solar_panel_output",
    "battery_discharge",
    "simulate_particle_collision",
    # Ollama router
    "dispatch",
    "route_to_ollama",
    "contains_ollama_handle",
    "strip_handles",
    "OLLAMA_BASE_URL",
    "DEFAULT_MODEL",
    "OLLAMA_HANDLES",
    "OllamaConnectionError",
    "OllamaRequestError",
]
