import asyncio
import logging
from typing import Any
from core.clock.clock import Clock
from core.clock.system_clock import SystemClock
from core.interfaces.transport import Transport
from core.models.message import Message
from collections.abc import Awaitable, Callable


logger = logging.getLogger(__name__)
MessageHandler = Callable[[Message], Awaitable[None]]

class Node:
    """An independent participant that sends and receives messages."""

    def __init__(self,node_id: str,transport: Transport,clock: Clock | None = None,) -> None:
        self.node_id = node_id
        self._transport = transport
        self._clock = clock if clock is not None else SystemClock()
        self._task: asyncio.Task[None] | None = None
        self._handler: MessageHandler | None = None

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

    
    async def run(self,handler: MessageHandler) -> None:
        """Continuously receive messages and pass them to a handler."""
        while True:
            message = await self.receive()
            try:
                await handler(message)
            except Exception :
                logger.exception("Node %s failed to process message %s", self.node_id, message.message_id,)


    
    @property
    def is_running(self) -> bool:
        """Return whether the node's processing task is active."""
        return self._task is not None and not self._task.done()


    async def start(self, handler: MessageHandler) -> None:
        """Start background message processing if it is not already running."""
        if self._task is not None and not self._task.done():
            return

        self._handler = handler
        self._task = asyncio.create_task(self.run(handler))


    async def stop(self) -> None:
        """Stop background message processing and wait for shutdown."""
        task = self._task

        if task is None:
            return

        self._task = None
        self._handler = None

        if not task.done():
            task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

