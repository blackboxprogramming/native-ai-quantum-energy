import math
import random

import pytest

from native_ai_quantum_energy.quantum_simulator import QuantumCircuit


def assert_complex_approx(value: complex, expected_real: float, expected_imag: float = 0.0) -> None:
    assert value.real == pytest.approx(expected_real)
    assert value.imag == pytest.approx(expected_imag)


def test_hadamard_creates_superposition():
    qc = QuantumCircuit(1)
    qc.apply_hadamard(0)
    state = qc.statevector()
    assert_complex_approx(state[0], 1 / math.sqrt(2))
    assert_complex_approx(state[1], 1 / math.sqrt(2))


def test_pauli_x_flips_qubit():
    qc = QuantumCircuit(1)
    qc.apply_pauli_x(0)
    state = qc.statevector()
    assert_complex_approx(state[0], 0.0)
    assert_complex_approx(state[1], 1.0)


def test_cnot_entangles_qubits():
    qc = QuantumCircuit(2)
    qc.apply_hadamard(0)
    qc.apply_cnot(0, 1)
    probs = qc.probabilities()
    assert probs[0] == pytest.approx(0.5, rel=1e-6)
    assert probs[3] == pytest.approx(0.5, rel=1e-6)
    assert probs[1] == pytest.approx(0.0, abs=1e-12)
    assert probs[2] == pytest.approx(0.0, abs=1e-12)


def test_measure_collapses_state(monkeypatch):
    qc = QuantumCircuit(1)
    qc.apply_hadamard(0)
    monkeypatch.setattr(random, "random", lambda: 0.25)
    outcome = qc.measure(0)
    assert outcome == 1
    state = qc.statevector()
    assert_complex_approx(state[0], 0.0)
    assert_complex_approx(state[1], 1.0)


def test_invalid_qubit_index():
    qc = QuantumCircuit(1)
    with pytest.raises(IndexError):
        qc.apply_hadamard(2)


def test_cnot_requires_distinct_qubits():
    qc = QuantumCircuit(2)
    with pytest.raises(ValueError):
        qc.apply_cnot(0, 0)
