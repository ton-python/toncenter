import typing as t
from dataclasses import dataclass, field
from enum import Enum

__all__ = [
    "DEFAULT_RECONNECT_POLICY",
    "DEFAULT_RETRY_POLICY",
    "NETWORK_BASE_URLS",
    "Network",
    "ReconnectPolicy",
    "RetryPolicy",
    "RetryRule",
    "Workchain",
]


class Network(int, Enum):
    """Available TON Center network environments."""

    MAINNET = -239
    TESTNET = -3


class Workchain(int, Enum):
    """TON blockchain workchain identifiers."""

    MASTERCHAIN = -1
    BASECHAIN = 0


NETWORK_BASE_URLS: t.Final[dict[Network, str]] = {
    Network.MAINNET: "https://toncenter.com",
    Network.TESTNET: "https://testnet.toncenter.com",
}


@dataclass(slots=True, frozen=True)
class RetryRule:
    """Single retry rule matching specific HTTP status codes.

    Attributes:
        statuses: HTTP status codes that trigger this rule.
        max_retries: maximum number of retries for these statuses.
        base_delay: initial delay in seconds before first retry.
        max_delay: upper bound for the delay after backoff.
        backoff_factor: multiplier applied to delay on each retry.

    """

    statuses: frozenset[int]
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    backoff_factor: float = 2.0

    def delay_for_attempt(self, attempt: int) -> float:
        """Calculate delay for the given attempt number.

        :param attempt: Zero-based attempt index.
        :return: Delay in seconds, capped by ``max_delay``.
        """
        delay = self.base_delay * (self.backoff_factor**attempt)
        return min(delay, self.max_delay)


@dataclass(slots=True, frozen=True)
class RetryPolicy:
    """Collection of retry rules.

    Attributes:
        rules: retry rules to apply.

    """

    rules: tuple[RetryRule, ...] = field(default_factory=tuple)

    def find_rule(self, status: int) -> RetryRule | None:
        """Find a retry rule matching the given status code.

        :param status: HTTP status code.
        :return: Matching `RetryRule`, or ``None``.
        """
        for rule in self.rules:
            if status in rule.statuses:
                return rule
        return None


@dataclass(slots=True, frozen=True)
class ReconnectPolicy:
    """Reconnection policy for streaming transports.

    Attributes:
        max_reconnects: maximum reconnection attempts, ``-1`` for unlimited.
        delay: initial delay in seconds before first reconnect.
        max_delay: upper bound for the delay after backoff.
        backoff_factor: multiplier applied to delay on each reconnect.

    """

    max_reconnects: int = 10
    delay: float = 2.0
    max_delay: float = 30.0
    backoff_factor: float = 2.0

    def delay_for_attempt(self, attempt: int) -> float:
        """Calculate delay for the given attempt number.

        :param attempt: Zero-based attempt index.
        :return: Delay in seconds, capped by ``max_delay``.
        """
        d = self.delay * (self.backoff_factor**attempt)
        return min(d, self.max_delay)


DEFAULT_RECONNECT_POLICY: t.Final[ReconnectPolicy] = ReconnectPolicy()

DEFAULT_RETRY_POLICY: t.Final[RetryPolicy] = RetryPolicy(
    rules=(
        RetryRule(
            statuses=frozenset({429}),
            max_retries=5,
            base_delay=0.3,
            max_delay=3.0,
            backoff_factor=2.0,
        ),
        RetryRule(
            statuses=frozenset({500, 502, 503, 504}),
            max_retries=3,
            base_delay=0.5,
            max_delay=5.0,
            backoff_factor=2.0,
        ),
    ),
)
