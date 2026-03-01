# Native AI Quantum Energy Lab

> **Zero-dependency quantum circuit simulation, energy modeling, and AI-native particle dynamics — built for production.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![npm](https://img.shields.io/badge/npm-native--ai--quantum--energy-red.svg)](https://www.npmjs.com/package/native-ai-quantum-energy)
[![License](https://img.shields.io/badge/license-Proprietary-lightgrey.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#6-testing)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Installation](#2-installation)
   - [Python (pip)](#python-pip)
   - [JavaScript (npm)](#javascript-npm)
3. [Quick Start](#3-quick-start)
4. [API Reference](#4-api-reference)
   - [Package Index](#package-index)
   - [QuantumCircuit](#quantumcircuit)
   - [Energy Simulator](#energy-simulator)
5. [Billing & Payments — Stripe](#5-billing--payments--stripe)
6. [Testing](#6-testing)
   - [Unit Tests](#unit-tests)
   - [End-to-End (E2E) Tests](#end-to-end-e2e-tests)
7. [Unsolved Problems Reference](#7-unsolved-problems-reference)
8. [Contributing](#8-contributing)
9. [License & Copyright](#9-license--copyright)

---

## 1. Overview

**Native AI Quantum Energy Lab** is a production-grade simulation platform that
combines a state-vector quantum circuit simulator, an energy and particle dynamics
library, and a reference index of the world's greatest unsolved mathematical
problems — all in a single, zero-dependency Python package that also ships as an
npm module.

| Feature | Detail |
|---|---|
| Quantum gates | H, X, Y, Z, S, T, Rx, Ry, Rz, CNOT, CZ |
| Energy models | Solar output, battery discharge, elastic collisions |
| Dependencies | **None** (pure Python standard library / pure JS) |
| Python support | 3.8 and later |
| Node.js support | 18 LTS and later |
| License | Proprietary — BlackRoad OS, Inc. |

---

## 2. Installation

### Python (pip)

```bash
pip install native-ai-quantum-energy
```

Requires **Python 3.8+**. No additional dependencies are needed.

### JavaScript (npm)

```bash
npm install native-ai-quantum-energy
```

Requires **Node.js 18 LTS** or later. The npm package exposes the same
simulation API via a lightweight Python-to-JS bridge.

```js
const { QuantumCircuit, solarPanelOutput } = require('native-ai-quantum-energy');
```

---

## 3. Quick Start

### Quantum circuit

```python
import math
from native_ai_quantum_energy import QuantumCircuit

# Two-qubit Bell-state preparation
qc = QuantumCircuit(2)
qc.apply_hadamard(0)
qc.apply_cnot(0, 1)

result = qc.measure_all()
print("Measurement outcome:", result)   # '00' or '11' with equal probability
print("State vector:", qc.statevector())
```

### Energy simulation

```python
from native_ai_quantum_energy import solar_panel_output, battery_discharge

# 100 W panel, 5 hours, 15 % efficiency -> energy in joules
energy_joules = solar_panel_output(100, 5, 0.15)
print("Energy produced (J):", energy_joules)   # 270000.0

# 2000 mAh battery, 500 mA load, 3 hours
remaining = battery_discharge(2000, 500, 3)
print("Remaining capacity (mAh):", remaining)  # 500.0
```

### Particle collision

```python
from native_ai_quantum_energy import simulate_particle_collision

v1_final, v2_final = simulate_particle_collision(m1=1.0, v1=2.0, m2=3.0, v2=0.0)
print(f"v1 = {v1_final:.4f} m/s,  v2 = {v2_final:.4f} m/s")
```

---

## 4. API Reference

### Package Index

```
native_ai_quantum_energy/
├── __init__.py               <- top-level re-exports
├── quantum_simulator.py      <- QuantumCircuit class
└── energy_simulator.py       <- energy & particle helpers
```

Top-level exports (importable directly from `native_ai_quantum_energy`):

| Symbol | Module | Description |
|---|---|---|
| `QuantumCircuit` | `quantum_simulator` | State-vector quantum circuit simulator |
| `solar_panel_output` | `energy_simulator` | Solar energy output in joules |
| `battery_discharge` | `energy_simulator` | Remaining battery capacity after discharge |
| `simulate_particle_collision` | `energy_simulator` | 1-D elastic collision velocities |

---

### QuantumCircuit

```python
class QuantumCircuit(num_qubits: int)
```

Constructs a circuit initialised to the |0...0> computational basis state.

#### Gate methods

| Method | Signature | Description |
|---|---|---|
| `apply_hadamard` | `(qubit)` | Hadamard (H) gate |
| `apply_pauli_x` | `(qubit)` | Pauli-X / NOT gate |
| `apply_pauli_y` | `(qubit)` | Pauli-Y gate |
| `apply_pauli_z` | `(qubit)` | Pauli-Z gate |
| `apply_s` | `(qubit)` | Phase (S) gate |
| `apply_t` | `(qubit)` | T (pi/8) gate |
| `apply_rx` | `(qubit, angle)` | Rotation about X axis by `angle` radians |
| `apply_ry` | `(qubit, angle)` | Rotation about Y axis by `angle` radians |
| `apply_rz` | `(qubit, angle)` | Rotation about Z axis by `angle` radians |
| `apply_cnot` | `(control, target)` | Controlled-NOT gate |
| `apply_cz` | `(control, target)` | Controlled-Z gate |

#### Measurement methods

| Method | Returns | Description |
|---|---|---|
| `measure(qubit)` | `int` | Measure one qubit; collapses state |
| `measure_all()` | `str` | Measure all qubits; returns bitstring |
| `measure_subset(qubits)` | `str` | Measure a subset of qubits |

#### State inspection

| Method | Returns | Description |
|---|---|---|
| `statevector()` | `List[complex]` | Copy of the current state vector |
| `probabilities()` | `List[float]` | Measurement probability per basis state |
| `amplitudes()` | `Tuple[complex, ...]` | Tuple view of current amplitudes |
| `initialize_statevector(amplitudes)` | `None` | Set state to a custom normalised vector |

---

### Energy Simulator

#### `solar_panel_output(power_watt, hours, efficiency=0.15) -> float`

Returns energy produced in **joules**: `power_watt x efficiency x hours x 3600`.

| Parameter | Type | Description |
|---|---|---|
| `power_watt` | `float` | Nominal panel power in watts (>= 0) |
| `hours` | `float` | Operating duration in hours (>= 0) |
| `efficiency` | `float` | Conversion efficiency, 0-1 (default 0.15) |

#### `battery_discharge(capacity_mAh, load_mA, hours) -> float`

Returns remaining capacity in **mAh** (minimum 0).

| Parameter | Type | Description |
|---|---|---|
| `capacity_mAh` | `float` | Initial capacity in mAh (>= 0) |
| `load_mA` | `float` | Constant current draw in mA (>= 0) |
| `hours` | `float` | Discharge duration in hours (>= 0) |

#### `simulate_particle_collision(m1, v1, m2, v2) -> Tuple[float, float]`

Returns `(v1_final, v2_final)` after a 1-D elastic collision.

| Parameter | Type | Description |
|---|---|---|
| `m1`, `m2` | `float` | Particle masses in kg (> 0) |
| `v1`, `v2` | `float` | Initial velocities in m/s |

---

## 5. Billing & Payments — Stripe

Native AI Quantum Energy Lab uses **[Stripe](https://stripe.com)** for subscription
billing and metered API usage. Follow the steps below to enable paid access.

### Setting up Stripe

1. Create a Stripe account at <https://dashboard.stripe.com/register>.
2. Obtain your **Secret Key** (`sk_live_...`) and **Publishable Key** (`pk_live_...`)
   from the Stripe Dashboard -> **Developers -> API keys**.
3. Set the keys as environment variables — never hard-code them in source files:

   ```bash
   export STRIPE_SECRET_KEY="sk_live_..."
   export STRIPE_PUBLISHABLE_KEY="pk_live_..."
   ```

4. Install the Stripe SDK alongside this package:

   ```bash
   # Python
   pip install stripe

   # Node.js / npm
   npm install stripe
   ```

### Creating a subscription (Python example)

```python
import os
import stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Create a customer
customer = stripe.Customer.create(email="user@example.com")

# Subscribe the customer to your price plan
subscription = stripe.Subscription.create(
    customer=customer["id"],
    items=[{"price": "price_XXXXXXXXXXXXXXXX"}],  # replace with your Price ID
)

print("Subscription status:", subscription["status"])
```

### Creating a subscription (Node.js / npm example)

```js
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const customer = await stripe.customers.create({ email: 'user@example.com' });

const subscription = await stripe.subscriptions.create({
  customer: customer.id,
  items: [{ price: 'price_XXXXXXXXXXXXXXXX' }],  // replace with your Price ID
});

console.log('Subscription status:', subscription.status);
```

### Webhook verification

Always verify Stripe webhook signatures to protect your endpoints:

```python
import os
import stripe
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"]
        )
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    # Handle event types here
    return '', 200
```

> **Security:** Store all Stripe keys in environment variables or a secrets
> manager. Never commit them to source control.

---

## 6. Testing

### Unit Tests

The project ships with a comprehensive `pytest` suite covering all public APIs.

```bash
# Install test runner
pip install pytest

# Run all unit tests
pytest

# Run with verbose output
pytest -v

# Run a specific test module
pytest tests/test_quantum_simulator.py
pytest tests/test_energy_simulator.py
```

All 22 tests pass without additional configuration.

### End-to-End (E2E) Tests

E2E tests exercise the full user-facing workflow — installation, import, circuit
execution and simulation output — in an isolated environment.

```bash
# 1. Create a clean virtual environment
python -m venv .venv-e2e
source .venv-e2e/bin/activate          # Windows: .venv-e2e\Scripts\activate

# 2. Install the package in the clean environment
pip install .

# 3. Run the E2E smoke test
python - <<'EOF'
import math
from native_ai_quantum_energy import (
    QuantumCircuit,
    solar_panel_output,
    battery_discharge,
    simulate_particle_collision,
)

# --- Quantum circuit E2E ---
qc = QuantumCircuit(2)
qc.apply_hadamard(0)
qc.apply_cnot(0, 1)
result = qc.measure_all()
assert result in ("00", "11"), f"Unexpected Bell result: {result}"

# --- Energy simulator E2E ---
energy = solar_panel_output(100, 5, 0.15)
assert math.isclose(energy, 270_000.0), f"Unexpected energy: {energy}"

remaining = battery_discharge(2000, 500, 3)
assert math.isclose(remaining, 500.0), f"Unexpected remaining: {remaining}"

# --- Particle collision E2E ---
v1f, v2f = simulate_particle_collision(1.0, 2.0, 1.0, 0.0)
assert math.isclose(v1f, 0.0, abs_tol=1e-9), f"Unexpected v1: {v1f}"
assert math.isclose(v2f, 2.0, abs_tol=1e-9), f"Unexpected v2: {v2f}"

print("All E2E checks passed.")
EOF

# 4. Deactivate and clean up
deactivate
```

#### npm / Node.js E2E

```bash
# Install the npm package
npm install native-ai-quantum-energy

# Run the Node.js smoke test
node -e "
const pkg = require('native-ai-quantum-energy');
const { QuantumCircuit, solarPanelOutput } = pkg;
const qc = new QuantumCircuit(2);
qc.applyHadamard(0);
qc.applyCnot(0, 1);
const result = qc.measureAll();
console.assert(['00','11'].includes(result), 'Unexpected result: ' + result);
console.log('npm E2E check passed.');
"
```

---

## 7. Unsolved Problems Reference

The file [`problems.md`](problems.md) contains concise summaries of ten of the
world's most renowned open problems in mathematics.

| # | Problem | Area |
|---|---|---|
| 1 | Riemann Hypothesis | Analytic number theory |
| 2 | P vs NP | Computational complexity |
| 3 | Navier-Stokes Existence and Smoothness | Fluid dynamics / PDE |
| 4 | Hodge Conjecture | Algebraic geometry |
| 5 | Yang-Mills Existence and Mass Gap | Quantum field theory |
| 6 | Birch and Swinnerton-Dyer Conjecture | Arithmetic geometry |
| 7 | Goldbach's Conjecture | Number theory |
| 8 | Twin Prime Conjecture | Number theory |
| 9 | Collatz Conjecture | Discrete mathematics |
| 10 | Euler-Mascheroni Constant Rationality | Analysis |

All six Clay Mathematics Institute Millennium Prize problems are included.

---

## 8. Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines, including
the BlackRoad Brand System, commit message conventions, and pull-request checklist.

**Quick summary:**

1. Fork the repository and create a feature branch.
2. Make your changes following the brand and coding guidelines.
3. Run the full test suite (`pytest`) and E2E checks before opening a PR.
4. Open a pull request with a clear description and screenshots for any UI changes.

---

## 9. License & Copyright

**Copyright © 2026 BlackRoad OS, Inc. All Rights Reserved.**

**CEO:** Alexa Amundson | **PROPRIETARY AND CONFIDENTIAL**

This software is NOT for commercial resale.

### Enterprise Scale

- 30,000 AI Agents
- 30,000 Human Employees
- CEO: Alexa Amundson

**Contact:** blackroad.systems@gmail.com

See [LICENSE](LICENSE) for complete terms.
