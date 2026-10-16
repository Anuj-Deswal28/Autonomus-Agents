from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4



@dataclass
class Message:
    sender_id : str
    topic : str
    timestamp : float
    payload : dict[str, Any] = field(default_factory=dict)
    message_id : str = field(default_factory= lambda : str(uuid4()))
    recipient_id : str | None = None
    correlation_id : str | None = None
