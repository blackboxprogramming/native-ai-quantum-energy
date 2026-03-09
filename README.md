# Native AI Quantum Energy Lab

Quantum circuit simulator, energy/particle simulations, and explorations of unsolved mathematical problems. Pure Python — no external dependencies.

## Modules

### Quantum Simulator

State-vector quantum circuit simulator supporting single-qubit gates (H, X, Y, Z, S, T, Rx, Ry, Rz), controlled operations (CNOT, CZ), custom statevector initialization, and partial measurement.

```python
from native_ai_quantum_energy.quantum_simulator import QuantumCircuit
import math

qc = QuantumCircuit(2)
qc.apply_hadamard(0)
qc.apply_ry(1, math.pi / 4)
qc.apply_cz(0, 1)

result = qc.measure_subset([0])
print("Measured:", result)
print("Statevector:", qc.statevector())
```

### Energy Simulator

Models for energy generation, battery discharge, and elastic particle collisions.

```python
from native_ai_quantum_energy.energy_simulator import solar_panel_output, battery_discharge

# 100W panel, 5 hours, 15% efficiency
energy = solar_panel_output(100, 5, 0.15)

# 2000mAh battery, 500mA load, 3 hours
remaining = battery_discharge(2000, 500, 3)
```

### Unsolved Problems

`problems.md` — summaries of 10 open mathematical problems including all Clay Millennium Prize problems (Riemann Hypothesis, P vs NP, etc.).

## Requirements

Python 3.8+ (stdlib only).

## Tests

```bash
pip install pytest
pytest
```

## Project Structure

```
native_ai_quantum_energy/
  quantum_simulator.py   # State-vector circuit simulator
  energy_simulator.py    # Energy and particle models
  __init__.py
tests/
  test_quantum_simulator.py
  test_energy_simulator.py
  conftest.py
problems.md              # 10 unsolved math problems
```

## License

Copyright 2026 BlackRoad OS, Inc. All rights reserved.
