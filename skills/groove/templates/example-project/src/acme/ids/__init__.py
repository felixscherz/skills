"""IDs: new identifiers, injected so the functional core never generates them."""

import uuid
from itertools import count
from typing import Protocol

__all__ = ["IdGenerator", "SequentialIdGenerator", "UuidIdGenerator"]


class IdGenerator(Protocol):
    def new_id(self) -> str: ...


class UuidIdGenerator:
    def __init__(self, prefix: str) -> None:
        self._prefix = prefix

    def new_id(self) -> str:
        return f"{self._prefix}{uuid.uuid4().hex}"


class SequentialIdGenerator:
    def __init__(self, prefix: str) -> None:
        self._prefix = prefix
        self._counter = count(1)

    def new_id(self) -> str:
        return f"{self._prefix}{next(self._counter):02d}"
