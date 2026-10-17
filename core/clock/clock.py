
from abc import ABC, abstractmethod


class Clock(ABC):
    """Interface for providing time to system components."""

    @abstractmethod
    def now(self) -> float:
        """Return the current time as a numeric timestamp."""
        raise NotImplementedError
