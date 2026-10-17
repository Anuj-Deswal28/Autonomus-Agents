
import asyncio

from runtime.node import Node
from transport.local.local_transport import LocalTransport


def test_nodes_can_communicate():
    async def run():
        transport = LocalTransport()

        robot_a = Node("robot-A", transport)
        robot_b = Node("robot-B", transport)

        sent_message = await robot_a.send(
            recipient_id="robot-B",
            topic="task.assigned",
            timestamp=1.0,
            payload={"task_id": "task-001"},
        )

        received_message = await robot_b.receive()

        assert received_message.message_id == sent_message.message_id
        assert received_message.sender_id == "robot-A"
        assert received_message.recipient_id == "robot-B"
        assert received_message.payload["task_id"] == "task-001"

    asyncio.run(run())


def test_node_sets_its_own_identity():
    async def run():
        transport = LocalTransport()
        robot_a = Node("robot-A", transport)

        message = await robot_a.send(
            recipient_id="robot-B",
            topic="robot.status",
            timestamp=1.0,
        )

        assert message.sender_id == "robot-A"

    asyncio.run(run())
