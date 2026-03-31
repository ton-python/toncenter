from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from collections.abc import Sequence


class KeyRotator:
    """Round-robin API key rotator.

    Cycles through a list of API keys, advancing to the next one
    on each ``rotate()`` call.

    :param keys: Sequence of API keys to rotate through.
    """

    def __init__(self, keys: Sequence[str]) -> None:
        self._keys = list(keys)
        self._index = 0

    @property
    def current(self) -> str:
        """Return the active API key without advancing.

        :return: Current API key.
        """
        return self._keys[self._index]

    def rotate(self) -> str:
        """Advance to the next key and return it.

        Wraps around to the first key after the last one.

        :return: New active API key.
        """
        self._index = (self._index + 1) % len(self._keys)
        return self._keys[self._index]
