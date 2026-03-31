from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from collections.abc import Sequence

from toncenter.rest.limiter import RateLimiter
from toncenter.types import ApiKey


class KeyRotator:
    """Round-robin key rotator with per-key rate limiting.

    Each ``ApiKey`` may carry its own ``rps_limit``.  Keys with
    ``rps_limit > 0`` get an individual ``RateLimiter``; others are
    unlimited on the client side.

    :param keys: Sequence of ``ApiKey`` instances to rotate through.
    """

    def __init__(self, keys: Sequence[ApiKey]) -> None:
        self._entries: list[tuple[str, RateLimiter | None]] = [
            (k.key, RateLimiter(rps=k.rps_limit, period=k.rps_period) if k.rps_limit > 0 else None) for k in keys
        ]
        self._index = 0

    @property
    def current_key(self) -> str:
        """Return the active API key without advancing."""
        return self._entries[self._index][0]

    @property
    def current_limiter(self) -> RateLimiter | None:
        """Return the rate limiter for the active key, or ``None``."""
        return self._entries[self._index][1]

    def rotate(self) -> str:
        """Advance to the next key and return it.

        Wraps around to the first key after the last one.

        :return: New active API key.
        """
        self._index = (self._index + 1) % len(self._entries)
        return self._entries[self._index][0]

    def __len__(self) -> int:
        return len(self._entries)
