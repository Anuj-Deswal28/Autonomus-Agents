
import asyncio

from core.models.message import Message
from transport.local.local_transport import LocalTransport


def test_message_delivery():
    async def run():
        transport = LocalTransport()

        message = Message(
            sender_id="robot-A",
            recipient_id="robot-B",
            topic="task.assigned",
            timestamp=1.0,
            payload={"task_id": "task-001"},
        )

        await transport.send(message)
        received = await transport.receive("robot-B")

        assert received.message_id == message.message_id
        assert received.payload["task_id"] == "task-001"

    asyncio.run(run())


def test_messages_are_delivered_to_correct_recipients():
    async def run():
        transport = LocalTransport()

        message_a = Message(
            sender_id="robot-A",
            recipient_id="robot-B",
            topic="robot.status",
            timestamp=1.0,
        )

        message_b = Message(
            sender_id="robot-C",
            recipient_id="robot-D",
            topic="robot.status",
            timestamp=2.0,
        )

        await transport.send(message_a)
        await transport.send(message_b)

        received = await transport.receive("robot-D")

        assert received.sender_id == "robot-C"

    asyncio.run(run())
