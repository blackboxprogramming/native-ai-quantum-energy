"""Quantum computing simulator for the Native AI Quantum Energy Lab.

This module implements a tiny quantum circuit simulator based on the
state‑vector formalism.  It supports constructing a register of qubits,
applying single‑qubit gates (Hadamard and Pauli‑X) and a controlled‑NOT (CNOT)
gate, and performing measurements.  The simulator is intentionally small and
focused on clarity rather than performance.

Example
-------

```python
from native_ai_quantum_energy.quantum_simulator import QuantumCircuit

# Create a two‑qubit circuit
qc = QuantumCircuit(2)

# Put qubit 0 into superposition and entangle it with qubit 1
qc.apply_hadamard(0)
qc.apply_cnot(0, 1)

# Measure both qubits; returns a bitstring like '00' or '11'
result = qc.measure_all()
print("Measurement outcomes:", result)
```

The code uses NumPy for linear algebra.  Install NumPy via `pip install numpy`.
"""

from __future__ import annotations

import math
import random
from typing import List

import numpy as np


class QuantumCircuit:
    """A minimal quantum circuit simulator based on state vectors."""

    # Gate matrices for convenience
    H_GATE: np.ndarray = (1 / math.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    X_GATE: np.ndarray = np.array([[0, 1], [1, 0]], dtype=complex)

    def __init__(self, num_qubits: int) -> None:
        if num_qubits < 1:
            raise ValueError("A circuit must have at least one qubit.")
        self.num_qubits = num_qubits
        # Start in the |0...0⟩ state
        dim = 2 ** num_qubits
        self.state: np.ndarray = np.zeros(dim, dtype=complex)
        self.state[0] = 1.0
        # Store measurement results
        self.measurements: List[int] = []

    def _apply_single_qubit_gate(self, gate: np.ndarray, qubit: int) -> None:
        """Apply a single‑qubit gate to the specified qubit.

        This constructs the full operator via tensor products of identities and
        the given gate, then applies it to the state vector.
        """
        if qubit < 0 or qubit >= self.num_qubits:
            raise IndexError("Qubit index out of range")
        # Build operator by Kronecker product: identity on other qubits, gate on target
        op = 1
        for i in range(self.num_qubits):
            if i == qubit:
                op = np.kron(op, gate)
            else:
                op = np.kron(op, np.eye(2))
        self.state = op @ self.state

    def apply_hadamard(self, qubit: int) -> None:
        """Apply a Hadamard gate (H) to one qubit."""
        self._apply_single_qubit_gate(self.H_GATE, qubit)

    def apply_pauli_x(self, qubit: int) -> None:
        """Apply a Pauli‑X (NOT) gate to one qubit."""
        self._apply_single_qubit_gate(self.X_GATE, qubit)

    def apply_cnot(self, control: int, target: int) -> None:
        """Apply a controlled‑NOT (CNOT) gate.

        The X gate is applied to the `target` qubit if and only if the
        `control` qubit is in state |1⟩.
        """
        if control == target:
            raise ValueError("Control and target must be different for CNOT")
        if any(q < 0 or q >= self.num_qubits for q in (control, target)):
            raise IndexError("Qubit index out of range")
        dimension = len(self.state)
        new_state = np.zeros_like(self.state)
        # For each basis state, flip the target bit if the control bit is 1
        for index, amplitude in enumerate(self.state):
            # Determine bit value of control qubit (most significant bit index 0)
            bit_val = (index >> (self.num_qubits - 1 - control)) & 1
            if bit_val == 1:
                # Flip target bit using XOR mask
                mask = 1 << (self.num_qubits - 1 - target)
                new_index = index ^ mask
            else:
                new_index = index
            new_state[new_index] += amplitude
        self.state = new_state

    def measure(self, qubit: int) -> int:
        """Measure a single qubit and collapse the state.

        Returns 0 or 1 according to the measured outcome.  After measurement,
        the state vector is collapsed (renormalized) consistent with the
        observed result.
        """
        if qubit < 0 or qubit >= self.num_qubits:
            raise IndexError("Qubit index out of range")
        prob0 = 0.0
        prob1 = 0.0
        mask = 1 << (self.num_qubits - 1 - qubit)
        # Compute probabilities by summing squared amplitudes
        for idx, amp in enumerate(self.state):
            if idx & mask:
                prob1 += abs(amp) ** 2
            else:
                prob0 += abs(amp) ** 2
        # Sample outcome
        rand = random.random()
        outcome = 1 if rand < prob1 else 0
        # Collapse state
        new_state = np.zeros_like(self.state)
        for idx, amp in enumerate(self.state):
            bit = 1 if idx & mask else 0
            if bit == outcome:
                new_state[idx] = amp
        # Renormalize
        norm = math.sqrt(prob1 if outcome == 1 else prob0)
        if norm > 0:
            new_state /= norm
        self.state = new_state
        return outcome

    def measure_all(self) -> str:
        """Measure all qubits sequentially, returning a bitstring.

        The measurement outcomes are stored in the instance attribute
        `measurements` and returned as a concatenated string (qubit 0 first).
        """
        self.measurements = []
        bits: List[int] = []
        for q in range(self.num_qubits):
            bit = self.measure(q)
            bits.append(bit)
            self.measurements.append(bit)
        return ''.join(str(b) for b in bits)

    def statevector(self) -> np.ndarray:
        """Return a copy of the current state vector."""
        return self.state.copy()
