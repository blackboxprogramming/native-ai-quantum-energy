import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from native_ai_quantum_energy.energy_simulator import solar_panel_output


def test_solar_panel_output_valid():
    energy = solar_panel_output(100, 2, 0.5)
    assert energy == pytest.approx(100 * 0.5 * 2 * 3600)


def test_solar_panel_output_negative_power():
    with pytest.raises(ValueError):
        solar_panel_output(-10, 1)


def test_solar_panel_output_negative_hours():
    with pytest.raises(ValueError):
        solar_panel_output(10, -1)
