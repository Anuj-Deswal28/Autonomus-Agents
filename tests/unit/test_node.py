
import asyncio

from runtime.node import Node
from transport.local.local_transport import LocalTransport
from core.clock.simulation_clock import SimulationClock


def test_nodes_can_communicate():
    async def run():
        transport = LocalTransport()

        robot_a = Node("robot-A", transport)
        robot_b = Node("robot-B", transport)

        sent_message = await robot_a.send(
            recipient_id="robot-B",
            topic="task.assigned",
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
        )

        assert message.sender_id == "robot-A"

    asyncio.run(run())


def test_node_uses_injected_clock():
    async def run():
        transport = LocalTransport()
        clock = SimulationClock(start_time=10.0)

        robot_a = Node(
            "robot-A",
            transport,
            clock=clock,
        )

        first_message = await robot_a.send(
            recipient_id="robot-B",
            topic="robot.status",
        )

        assert first_message.timestamp == 10.0

        clock.advance(2.5)

        second_message = await robot_a.send(
            recipient_id="robot-B",
            topic="robot.status",
        )

        assert second_message.timestamp == 12.5

    asyncio.run(run())


def test_node_run_processes_incoming_messages():
    async def run():
        transport = LocalTransport()
        robot_a = Node("robot-A", transport)
        robot_b = Node("robot-B", transport)

        processed_messages = []

        async def handler(message):
            processed_messages.append(message)

        # Start robot B's continuous processing loop.
        task = asyncio.create_task(robot_b.run(handler))

        try:
            # Send two messages to robot B.
            await robot_a.send(
                recipient_id="robot-B",
                topic="robot.status",
                payload={"status": "ready"},
            )

            await robot_a.send(
                recipient_id="robot-B",
                topic="task.assigned",
                payload={"task_id": "task-001"},
            )

            # Wait until both messages have been processed.
            for _ in range(100):
                if len(processed_messages) == 2:
                    break
                await asyncio.sleep(0.01)

            assert len(processed_messages) == 2
            assert processed_messages[0].topic == "robot.status"
            assert processed_messages[1].topic == "task.assigned"

        finally:
            # Stop the infinite processing loop.
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

    asyncio.run(run())


def test_node_continues_after_handler_error():
    async def run():
        transport = LocalTransport()
        robot_a = Node("robot-A", transport)
        robot_b = Node("robot-B", transport)

        processed_topics = []

        async def handler(message):
            if message.topic == "task.invalid":
                raise ValueError("Invalid task")

            processed_topics.append(message.topic)

        task = asyncio.create_task(robot_b.run(handler))

        try:
            await robot_a.send(
                recipient_id="robot-B",
                topic="task.invalid",
            )

            await robot_a.send(
                recipient_id="robot-B",
                topic="robot.status",
            )

            for _ in range(100):
                if "robot.status" in processed_topics:
                    break
                await asyncio.sleep(0.01)

            assert processed_topics == ["robot.status"]

        finally:
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

    asyncio.run(run())


