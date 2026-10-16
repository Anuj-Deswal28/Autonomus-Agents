"""Wall-clock implementation for live execution."""

import time

from .interface import Clock


class SystemClock(Clock):
    def now(self) -> float:
        return time.time()
