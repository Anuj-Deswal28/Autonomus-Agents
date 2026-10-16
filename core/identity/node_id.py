"""Stable node identifier helpers."""

from uuid import uuid4


def new_node_id() -> str:
    return str(uuid4())
