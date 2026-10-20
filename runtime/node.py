
from core.clock.clock import Clock
from core.clock.system_clock import SystemClock
from core.interfaces.transport import Transport
from core.models.message import Message
from collections.abc import Awaitable, Callable


class Node:
    """An independent participant that sends and receives messages."""

    def __init__(self,node_id: str,transport: Transport,clock: Clock | None = None,) -> None:
        self.node_id = node_id
        self._transport = transport
        self._clock = clock if clock is not None else SystemClock()

    async def send(self,recipient_id: str,topic: str,payload: dict | None = None,correlation_id: str | None = None,) -> Message:
        """Create and send a timestamped message."""
        message = Message(
            sender_id=self.node_id,
            recipient_id=recipient_id,
            topic=topic,
            timestamp=self._clock.now(),
            payload=payload if payload is not None else {},
            correlation_id=correlation_id,
        )

        await self._transport.send(message)
        return message

    async def receive(self) -> Message:
        """Receive the next message addressed to this node."""
        return await self._transport.receive(self.node_id)

    
    async def run(self,handler: Callable[[Message], Awaitable[None]],) -> None:
        """Continuously receive messages and pass them to a handler."""
        while True:
            message = await self.receive()
            try:
                await handler(message)
            except Exception as error:
                print(
                    f"Node {self.node_id} failed to process "
                    f"message {message.message_id}: {error}"
                )



