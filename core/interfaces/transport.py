
from abc import ABC, abstractmethod

from core.models.message import Message


class Transport(ABC):
    """Interface for delivering messages between nodes."""

    @abstractmethod
    async def send(self, message: Message) -> None:
        """Deliver a message to its intended recipient."""
        raise NotImplementedError

    @abstractmethod
    async def receive(self, recipient_id: str) -> Message:
        """Wait for and return the next message for a node."""
        raise NotImplementedError
