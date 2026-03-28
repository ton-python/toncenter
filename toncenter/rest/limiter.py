import asyncio
import time


class RateLimiter:
    """Sliding-window rate limiter for async requests.

    :param rps: Maximum requests per second.
    :param period: Time window in seconds (default ``1.0``).
    """

    def __init__(self, rps: int, period: float = 1.0) -> None:
        self._rps = rps
        self._period = period
        self._timestamps: list[float] = []
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request slot is available."""
        while True:
            async with self._lock:
                now = time.monotonic()
                cutoff = now - self._period
                self._timestamps = [ts for ts in self._timestamps if ts > cutoff]

                if len(self._timestamps) < self._rps:
                    self._timestamps.append(now)
                    return

                sleep_for = self._timestamps[0] - cutoff

            await asyncio.sleep(sleep_for)
