"""Clock interface used by modules and runtime."""

from abc import ABC, abstractmethod


class Clock(ABC):
    @abstractmethod
    def now(self) -> float:
        """Return the current clock value in seconds."""
        raise NotImplementedError
