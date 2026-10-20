
import pytest

from core.clock.simulation_clock import SimulationClock
from core.clock.system_clock import SystemClock


def test_simulation_clock_starts_at_given_time():
    clock = SimulationClock(start_time=10.0)

    assert clock.now() == 10.0


def test_simulation_clock_advances():
    clock = SimulationClock(start_time=0.0)

    clock.advance(2.5)
    clock.advance(1.0)

    assert clock.now() == 3.5


def test_simulation_clock_rejects_negative_advance():
    clock = SimulationClock(start_time=5.0)

    with pytest.raises(ValueError):
        clock.advance(-1.0)

    assert clock.now() == 5.0


def test_system_clock_returns_numeric_timestamp():
    clock = SystemClock()

    timestamp = clock.now()

    assert isinstance(timestamp, float)
    assert timestamp > 0.0
