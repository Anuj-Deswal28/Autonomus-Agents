"""Minimal manually advanced simulation clock."""

from .interface import Clock


class SimulationClock(Clock):
    def __init__(self, start: float = 0.0) -> None:
        self._time = float(start)

    def now(self) -> float:
        return self._time

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("Simulation time cannot move backwards")
        self._time += seconds
