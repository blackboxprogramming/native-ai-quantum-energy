#!/usr/bin/env python3
"""Entry point demo for the Native AI Quantum Energy Lab.

Run with:
    python main.py
"""

import math

from native_ai_quantum_energy import (
    QuantumCircuit,
    battery_discharge,
    simulate_particle_collision,
    solar_panel_output,
)


def demo_quantum_circuit() -> None:
    """Run a small quantum circuit and display probabilities."""
    print("=" * 60)
    print("Quantum Circuit Demo")
    print("=" * 60)

    qc = QuantumCircuit(2)
    qc.apply_hadamard(0)
    qc.apply_cnot(0, 1)

    print("\nBell state (|00> + |11>) / sqrt(2)")
    print(f"  State vector: {qc.statevector()}")
    print(f"  Probabilities: {qc.probabilities()}")

    result = qc.measure_all()
    print(f"  Measurement:   {result}")
    print()

    qc3 = QuantumCircuit(3)
    qc3.apply_hadamard(0)
    qc3.apply_cnot(0, 1)
    qc3.apply_cnot(0, 2)

    print("GHZ state (|000> + |111>) / sqrt(2)")
    probs = qc3.probabilities()
    for i, p in enumerate(probs):
        if p > 1e-10:
            label = format(i, f"0{qc3.num_qubits}b")
            print(f"  |{label}>  probability = {p:.4f}")

    result = qc3.measure_all()
    print(f"  Measurement:   {result}")
    print()

    qc_rot = QuantumCircuit(1)
    qc_rot.apply_ry(0, math.pi / 3)
    print("Ry(pi/3) on |0>:")
    print(f"  P(|0>)={qc_rot.probabilities()[0]:.4f}, P(|1>)={qc_rot.probabilities()[1]:.4f}")
    print()


def demo_energy_simulation() -> None:
    """Run the energy simulation functions and display results."""
    print("=" * 60)
    print("Energy Simulation Demo")
    print("=" * 60)

    energy_j = solar_panel_output(300, 6, 0.20)
    print(f"\nSolar panel: 300W, 6h, 20% eff -> {energy_j:,.0f} J ({energy_j/3.6e6:.2f} kWh)")

    remaining = battery_discharge(5000, 800, 4)
    print(f"Battery: 5000mAh, 800mA load, 4h -> {remaining:.0f} mAh remaining")

    m1, v1, m2, v2 = 2.0, 3.0, 1.0, -1.0
    v1f, v2f = simulate_particle_collision(m1, v1, m2, v2)
    print(f"Collision: ({m1}kg@{v1}m/s) vs ({m2}kg@{v2}m/s) -> {v1f:.2f}, {v2f:.2f} m/s")

    p_before = m1 * v1 + m2 * v2
    p_after = m1 * v1f + m2 * v2f
    print(f"  Momentum conserved: {math.isclose(p_before, p_after)}")
    print()


if __name__ == "__main__":
    demo_quantum_circuit()
    demo_energy_simulation()
    print("Done.")
