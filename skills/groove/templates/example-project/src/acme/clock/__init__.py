"""Clock: the current time, injected so the functional core never reads it."""

from datetime import UTC, datetime, timedelta
from typing import Protocol

__all__ = ["Clock", "FakeClock", "SystemClock"]


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class FakeClock:
    def __init__(self, start: datetime) -> None:
        self._now = start

    def now(self) -> datetime:
        return self._now

    def advance(self, by: timedelta) -> None:
        self._now += by
