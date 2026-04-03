from __future__ import annotations

import typing as t

import aiohttp

from toncenter.client import BaseClient
from toncenter.exceptions import ToncenterTooManyRequestsError
from toncenter.rest.limiter import RateLimiter
from toncenter.rest.rotator import KeyRotator
from toncenter.rest.v2.mixin import V2Mixin
from toncenter.rest.v3.mixin import V3Mixin
from toncenter.types import (
    DEFAULT_RETRY_POLICY,
    NETWORK_BASE_URLS,
    ApiKey,
    Network,
    RetryPolicy,
)

__all__ = ["ToncenterRestClient"]

_T = t.TypeVar("_T")


class ToncenterRestClient(BaseClient):
    """Async client for the TON Center REST API (v2 and v3)."""

    def __init__(
        self,
        api_key: str | ApiKey | list[ApiKey] = "",
        network: Network = Network.MAINNET,
        *,
        base_url: str | None = None,
        timeout: float = 10.0,
        session: aiohttp.ClientSession | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        rps_limit: int | None = None,
        rps_period: float | None = None,
        retry_policy: RetryPolicy | None = DEFAULT_RETRY_POLICY,
    ) -> None:
        """Initialize the TON Center client.

        :param api_key: TON Center API key, ``ApiKey`` with per-key rate limit,
            or a list of ``ApiKey`` for automatic rotation on HTTP 429.
            Optional — without a key requests are throttled to ~1 RPS.
            Get one via @toncenter bot on Telegram.
        :param network: Target network (``Network.MAINNET`` or ``Network.TESTNET``).
        :param base_url: Custom base URL (overrides ``network``).
        :param timeout: Request timeout in seconds.
        :param session: Optional external ``aiohttp.ClientSession``.
            When provided, the client will not close it — the caller
            is responsible for managing its lifecycle.
        :param headers: Additional HTTP headers sent with every request.
        :param cookies: Additional cookies sent with every request.
        :param rps_limit: Maximum requests per second.
            Used only when ``api_key`` is a plain string.
            ``None`` (default) — auto: ``1`` RPS without a key,
            disabled with a key. ``0`` — explicitly disabled.
        :param rps_period: Rate-limiter window in seconds.
            Used only when ``api_key`` is a plain string.
            ``None`` (default) — ``1.2`` s when auto-limiting
            without a key, ``1.0`` s when ``rps_limit`` is set
            explicitly.
        :param retry_policy: Retry policy, or ``None`` to disable retries.
        """
        if isinstance(api_key, list):
            self._key_rotator: KeyRotator | None = KeyRotator(api_key) if api_key else None
            initial_key = api_key[0].key if api_key else ""
            self._rate_limiter: RateLimiter | None = None
        elif isinstance(api_key, ApiKey):
            self._key_rotator = None
            initial_key = api_key.key
            self._rate_limiter = (
                RateLimiter(rps=api_key.rps_limit, period=api_key.rps_period) if api_key.rps_limit > 0 else None
            )
        else:
            self._key_rotator = None
            initial_key = api_key
            if rps_limit is None:
                self._rate_limiter = RateLimiter(rps=1, period=rps_period or 1.2) if not api_key else None
            elif rps_limit > 0:
                self._rate_limiter = RateLimiter(rps=rps_limit, period=rps_period or 1.0)
            else:
                self._rate_limiter = None

        super().__init__(
            api_key=initial_key,
            base_url=base_url or NETWORK_BASE_URLS[network],
            timeout=timeout,
            session=session,
            headers=headers,
            cookies=cookies,
            retry_policy=retry_policy,
        )
        self._v2 = V2Mixin(self)
        self._v3 = V3Mixin(self)

    @property
    def v2(self) -> V2Mixin:
        """Access API v2 resource groups.

        :return: ``V2Mixin`` instance with v2 resources.
        """
        return self._v2

    @property
    def v3(self) -> V3Mixin:
        """Access API v3 resource groups.

        :return: ``V3Mixin`` instance with v3 resources.
        """
        return self._v3

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: type[_T] | None = None,
    ) -> _T | t.Any:
        """Execute an HTTP request with retry and rate limiting.

        When multiple ``ApiKey`` instances are configured, rotates to the
        next key after all retries for the current key are exhausted on
        HTTP 429.  Each key uses its own ``RateLimiter``.

        :param method: HTTP method (``GET``, ``POST``, etc.).
        :param path: API path.
        :param params: Query parameters.
        :param body: JSON request body.
        :param headers: Additional request headers.
        :param response_model: Pydantic model to parse response into.
        :return: Parsed model instance, raw dict, or ``None``.
        """
        if self._key_rotator is None:
            if self._rate_limiter:
                await self._rate_limiter.acquire()
            return await super().request(
                method, path, params=params, body=body, headers=headers, response_model=response_model
            )

        last_exc: ToncenterTooManyRequestsError | None = None

        for _ in range(len(self._key_rotator)):
            limiter = self._key_rotator.current_limiter
            if limiter:
                await limiter.acquire()
            key_headers = {**(headers or {}), "X-API-Key": self._key_rotator.current_key}

            try:
                return await super().request(
                    method, path, params=params, body=body, headers=key_headers, response_model=response_model
                )
            except ToncenterTooManyRequestsError as exc:
                last_exc = exc
                self._key_rotator.rotate()

        raise last_exc  # type: ignore[misc]
