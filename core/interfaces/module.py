"""Base contract for P-7 modules."""

from abc import ABC, abstractmethod
from typing import Any


class P7Module(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique module name."""
        raise NotImplementedError

    @abstractmethod
    async def start(self, context: Any) -> None:
        """Start the module using shared P-7 services."""
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        """Stop the module and release resources."""
        raise NotImplementedError
