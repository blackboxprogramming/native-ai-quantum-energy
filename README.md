# Native AI Quantum Energy Lab

**Native AI Quantum Energy Lab** is an experimental educational project that combines a simple
quantum‑computing simulator with an exploration of long‑standing unsolved mathematical
problems and a small library of energy and particle simulations.  It is inspired by the
idea of building a “native AI quantum computer” – a software system capable of running
quantum circuits, thinking about deep mathematical questions and even modeling energy
transfer and particle interactions on a classical computer.

## What’s inside?

This repository contains two main simulation modules and a document explaining
ten famous unsolved problems in mathematics:

1. **Quantum Computing Simulation** – a minimal yet functional simulator for quantum
   circuits written in pure Python (found in `quantum_simulator.py`).  The simulator
   supports a small set of single‑qubit gates (Hadamard and Pauli‑X), a
   two‑qubit controlled‑NOT (CNOT) gate and measurement.  You can create
   circuits, apply gates, and measure qubits to observe the probabilistic outcomes
   expected from quantum mechanics.  The code uses the vector–state model and
   linear algebra via NumPy.

2. **Energy and Particle Simulation** – a simple set of utilities (in
   `energy_simulator.py`) that model energy generation and consumption as well as
   basic particle interactions.  Functions include:

   * `solar_panel_output(power_watt, hours, efficiency)` – computes the energy
     produced by a solar panel over a number of hours.
   * `battery_discharge(capacity_mAh, load_mA, hours)` – estimates the remaining
     battery capacity after discharging at a given load.
   * `simulate_particle_collision(m1, v1, m2, v2)` – performs a simple
     one‑dimensional elastic collision between two particles and returns their
     post‑collision velocities.

   These routines are not intended to be accurate physical simulations but
   demonstrate how one might model energy and particle dynamics in software.

3. **Unsolved Mathematical Problems** – the file `problems.md` contains short
   summaries of ten of the world’s most renowned open problems.  Each
   problem entry includes a succinct description and, where appropriate, links
   to authoritative sources for further reading.  The list includes all of the
   Clay Mathematics Institute (CMI) Millennium Prize problems (such as the
   Riemann Hypothesis and P vs NP) plus additional conjectures from number
   theory and analysis.

## Getting started

To use the simulators you need Python 3 and NumPy installed.  Clone this
repository and run the Python modules directly, or import the functions into
your own scripts.  For example, to create a simple quantum circuit:

```python
from native_ai_quantum_energy.quantum_simulator import QuantumCircuit

# Create a two‑qubit circuit
qc = QuantumCircuit(2)

# Put the first qubit into superposition and entangle with the second qubit
qc.apply_hadamard(0)
qc.apply_cnot(0, 1)

# Measure both qubits
qc.measure_all()

print("Measurement results:", qc.measurements)

Similarly, to simulate energy production:

```python
from native_ai_quantum_energy.energy_simulator import solar_panel_output, battery_discharge

# 100 W solar panel running for 5 hours at 15 % efficiency
energy_joules = solar_panel_output(100, 5, 0.15)
print("Energy produced (J):", energy_joules)

# Battery with 2000 mAh capacity delivering 500 mA for 3 hours
remaining = battery_discharge(2000, 500, 3)
print("Remaining capacity (mAh):", remaining)
```

## Discla

The “harness energy and particles” portion of this project is a purely digital
exercise.  The simulations here do **not** allow a computer to collect real
energy or manipulate physical particles; they simply model these processes in
software for educational purposes.  Likewise, the unsolved problems summaries
are provided for learning and inspiration and do not offer solutions to those
problems.
