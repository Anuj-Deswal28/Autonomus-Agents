from core.models.message import Message

def test_message_cration():
    message = Message(
        sender_id= "warehouse.robot.A",
        topic="task.assigned",
        timestamp= 1.0,
        payload={"task_id" : "task-001"},
    )

    assert message.sender_id == "warehouse.robot.A"
    assert message.topic == "task.assigned"
    assert message.payload["task_id"] == "task-001"
    assert message.message_id

def test_messages_have_unique_ids():
    first = Message("robot-A", "robot.status", 1.0)
    second = Message("robot-B", "robot.status", 1.0)

    assert first.message_id != second.message_id