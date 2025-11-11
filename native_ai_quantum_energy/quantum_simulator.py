"""Quantum computing simulator for the Native AI Quantum Energy Lab.

This module implements a tiny quantum circuit simulator based on the
state-vector formalism.  It supports constructing a register of qubits,
applying single-qubit gates (Hadamard and Pauli-X) and a controlled-NOT (CNOT)
gate, and performing measurements.  The simulator is intentionally small and
focused on clarity rather than performance.

Example
-------

```python
from native_ai_quantum_energy.quantum_simulator import QuantumCircuit

# Create a two-qubit circuit
qc = QuantumCircuit(2)

# Put qubit 0 into superposition and entangle it with qubit 1
qc.apply_hadamard(0)
qc.apply_cnot(0, 1)

# Measure both qubits; returns a bitstring like '00' or '11'
result = qc.measure_all()
print("Measurement outcomes:", result)
```

The implementation is written using only the Python standard library so it can
run without third-party numerical dependencies.
"""

from __future__ import annotations

import math
import random
from typing import List, Sequence, Tuple

GateMatrix = Tuple[Tuple[complex, complex], Tuple[complex, complex]]


class QuantumCircuit:
    """A minimal quantum circuit simulator based on state vectors."""

    # Gate matrices for convenience
    H_GATE: GateMatrix = (
        (1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j),
        (1 / math.sqrt(2) + 0j, -(1 / math.sqrt(2)) + 0j),
    )
    X_GATE: GateMatrix = ((0 + 0j, 1 + 0j), (1 + 0j, 0 + 0j))

    def __init__(self, num_qubits: int) -> None:
        if num_qubits < 1:
            raise ValueError("A circuit must have at least one qubit.")
        self.num_qubits = num_qubits
        # Start in the |0...0⟩ state
        dim = 2 ** num_qubits
        self.state: List[complex] = [0j] * dim
        self.state[0] = 1.0 + 0j
        # Store measurement results
        self.measurements: List[int] = []

    def _apply_single_qubit_gate(self, gate: GateMatrix, qubit: int) -> None:
        """Apply a single-qubit gate to the specified qubit.

        This constructs the full operator implicitly by iterating over the
        amplitudes associated with the target qubit and updating the state
        vector in place.
        """

        if qubit < 0 or qubit >= self.num_qubits:
            raise IndexError("Qubit index out of range")

        mask = 1 << (self.num_qubits - 1 - qubit)
        new_state = self.state.copy()
        for index in range(len(self.state)):
            if index & mask:
                continue  # processed as the partner of an earlier index
            partner = index | mask
            amp0 = self.state[index]
            amp1 = self.state[partner]
            new_state[index] = gate[0][0] * amp0 + gate[0][1] * amp1
            new_state[partner] = gate[1][0] * amp0 + gate[1][1] * amp1
        self.state = new_state

    def apply_hadamard(self, qubit: int) -> None:
        """Apply a Hadamard gate (H) to one qubit."""

        self._apply_single_qubit_gate(self.H_GATE, qubit)

    def apply_pauli_x(self, qubit: int) -> None:
        """Apply a Pauli-X (NOT) gate to one qubit."""

        self._apply_single_qubit_gate(self.X_GATE, qubit)

    def apply_cnot(self, control: int, target: int) -> None:
        """Apply a controlled-NOT (CNOT) gate.

        The X gate is applied to the ``target`` qubit if and only if the
        ``control`` qubit is in state |1⟩.
        """

        if control == target:
            raise ValueError("Control and target must be different for CNOT")
        if any(q < 0 or q >= self.num_qubits for q in (control, target)):
            raise IndexError("Qubit index out of range")

        control_mask = 1 << (self.num_qubits - 1 - control)
        target_mask = 1 << (self.num_qubits - 1 - target)
        new_state = [0j] * len(self.state)
        for index, amplitude in enumerate(self.state):
            if index & control_mask:
                new_index = index ^ target_mask
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
        for idx, amp in enumerate(self.state):
            if idx & mask:
                prob1 += abs(amp) ** 2
            else:
                prob0 += abs(amp) ** 2

        rand = random.random()
        outcome = 1 if rand < prob1 else 0

        new_state = [0j] * len(self.state)
        for idx, amp in enumerate(self.state):
            bit = 1 if idx & mask else 0
            if bit == outcome:
                new_state[idx] = amp

        norm = math.sqrt(prob1 if outcome == 1 else prob0)
        if norm > 0:
            new_state = [amp / norm for amp in new_state]

        self.state = new_state
        return outcome

    def measure_all(self) -> str:
        """Measure all qubits sequentially, returning a bitstring.

        The measurement outcomes are stored in the instance attribute
        ``measurements`` and returned as a concatenated string (qubit 0 first).
        """

        self.measurements = []
        bits: List[int] = []
        for q in range(self.num_qubits):
            bit = self.measure(q)
            bits.append(bit)
            self.measurements.append(bit)
        return "".join(str(b) for b in bits)

    def statevector(self) -> List[complex]:
        """Return a copy of the current state vector."""

        return self.state.copy()

    def probabilities(self) -> List[float]:
        """Return measurement probabilities for each basis state."""

        return [abs(amp) ** 2 for amp in self.state]

    def amplitudes(self) -> Sequence[complex]:
        """Return a tuple view of the current amplitudes."""

        return tuple(self.state)
