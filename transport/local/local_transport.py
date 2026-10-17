
import asyncio

from core.interfaces.transport import Transport
from core.models.message import Message

"""we create an dictionary which act as central inbox for all messages inside dictionary all nodes will have their own inbox as asynco queue , if any node want to send a message it will put the message on recipient inbox queue and when a node want to recieve message it will see the its inbox in dictionary and get the message"""

class LocalTransport(Transport):
    """Deliver messages between nodes within one process."""

    def __init__(self) -> None:
        self._queues: dict[str, asyncio.Queue[Message]] = {}


    """this is a common function used by both sender and reciever to get the inbox of reciepient/self, it uses reciepient id , when sending an message we will pass reciepient id and when recieving an message we will pass self id"""
    def _get_queue(self, recipient_id: str) -> asyncio.Queue[Message]:
        """Get the incoming message queue for a node."""
        if recipient_id not in self._queues:
            self._queues[recipient_id] = asyncio.Queue()

        return self._queues[recipient_id]

    async def send(self, message: Message) -> None:
        """Place a message in the recipient's incoming queue."""
        if message.recipient_id is None:
            raise ValueError("Message must have a recipient_id.")

        queue = self._get_queue(message.recipient_id)
        await queue.put(message)

    async def receive(self, recipient_id: str) -> Message:
        """Wait until the node has a message to receive."""
        queue = self._get_queue(recipient_id)
        return await queue.get()
