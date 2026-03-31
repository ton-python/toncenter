from __future__ import annotations

import asyncio
import json
import typing as t

if t.TYPE_CHECKING:
    import types

import aiohttp
from pydantic import TypeAdapter, ValidationError

from toncenter.exceptions import (
    ToncenterConnectionError,
    ToncenterError,
    ToncenterRetryError,
    ToncenterSessionError,
    ToncenterValidationError,
    raise_for_status,
)
from toncenter.rotator import KeyRotator
from toncenter.types import (
    DEFAULT_RETRY_POLICY,
    RetryPolicy,
)

__all__ = ["BaseClient"]

T = t.TypeVar("T")
_Self = t.TypeVar("_Self", bound="BaseClient")

_adapter_cache: dict[t.Any, TypeAdapter[t.Any]] = {}


def _get_adapter(model: t.Any) -> TypeAdapter[t.Any]:
    """Return a cached ``TypeAdapter`` for the given model."""
    adapter = _adapter_cache.get(model)
    if adapter is None:
        adapter = TypeAdapter(model)
        _adapter_cache[model] = adapter
    return adapter


class BaseClient:
    """Base async HTTP client with session management and retry."""

    def __init__(
        self,
        api_key: str | list[str] = "",
        base_url: str = "",
        *,
        timeout: float = 10.0,
        session: aiohttp.ClientSession | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        retry_policy: RetryPolicy | None = DEFAULT_RETRY_POLICY,
    ) -> None:
        """Initialize the base HTTP client.

        :param api_key: TON Center API key or a list of keys for automatic rotation
            on HTTP 429. Optional for REST — without a key requests are throttled
            to ~1 RPS. Get one via @toncenter bot on Telegram.
        :param base_url: Base URL for all requests.
        :param timeout: Request timeout in seconds.
        :param session: Optional external ``aiohttp.ClientSession``.
            When provided, the client will not close it — the caller
            is responsible for managing its lifecycle.
        :param headers: Additional HTTP headers sent with every request.
        :param cookies: Additional cookies sent with every request.
        :param retry_policy: Retry policy, or ``None`` to disable retries.
        """
        if isinstance(api_key, list):
            self._key_rotator: KeyRotator | None = KeyRotator(api_key) if api_key else None
            self._api_key = api_key[0] if api_key else ""
        else:
            self._key_rotator = None
            self._api_key = api_key
        self._base_url = base_url.rstrip("/")

        self._headers = headers or {}
        self._cookies = cookies or {}
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: aiohttp.ClientSession | None = session

        self._is_external_session = session is not None
        self._retry_policy = retry_policy

    async def create_session(self: _Self) -> _Self:
        """Create an ``aiohttp.ClientSession`` for making requests.

        If an external session was provided via the ``session`` parameter,
        this method does nothing — the external session is used as-is.

        :return: This client instance.
        """
        if self._session is not None and self._session.closed and self._is_external_session:
            raise ToncenterSessionError(
                "External session is closed. Provide a new session or create the client without an external session."
            )
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers=self._build_headers(),
                cookies=self._cookies,
                timeout=self._timeout,
            )
            self._is_external_session = False
        return self

    async def close_session(self) -> None:
        """Close the ``aiohttp.ClientSession``.

        If the session was provided externally, it is not closed here —
        the caller is responsible for managing its lifecycle.
        """
        if self._session and not self._session.closed and not self._is_external_session:
            await self._session.close()
            await asyncio.sleep(0)
            self._session = None

    async def __aenter__(self: _Self) -> _Self:
        """Enter the async context manager."""
        await self.create_session()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Exit the async context manager."""
        await self.close_session()

    def _build_headers(self) -> dict[str, str]:
        """Build default request headers.

        :return: Merged headers dict.
        """
        base: dict[str, str] = {"Accept": "application/json"}
        if self._api_key:
            base["X-API-Key"] = self._api_key
        base.update(self._headers)
        return base

    @staticmethod
    def _parse_body(text: str) -> t.Any:
        """Parse response text as JSON.

        :param text: Raw response text.
        :return: Parsed data, or ``None`` if parsing fails.
        """
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    @t.overload
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: type[T],
    ) -> T: ...

    @t.overload
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: None = None,
    ) -> t.Any: ...

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: type[T] | None = None,
    ) -> T | t.Any:
        """Execute an HTTP request with retry.

        :param method: HTTP method (``GET``, ``POST``, etc.).
        :param path: API path.
        :param params: Query parameters.
        :param body: JSON request body.
        :param headers: Additional request headers.
        :param response_model: Pydantic model to parse response into.
        :return: Parsed model instance, raw dict, or ``None``.
        """
        url = f"{self._base_url}{path}"
        if params:
            params = {k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items() if v is not None}
        if headers:
            headers = {k: str(v) for k, v in headers.items() if v is not None}

        if self._session is None or self._session.closed:
            name = self.__class__.__name__
            raise ToncenterSessionError(
                f"Session is not created. "
                f"Call 'await {name}(...).create_session()' "
                f"or use 'async with {name}(...) as client:'"
            )

        session = self._session
        last_error: Exception | None = None
        last_status: int | None = None
        max_attempts = 1

        if self._retry_policy:
            max_rule_retries = max(
                (r.max_retries for r in self._retry_policy.rules),
                default=0,
            )
            max_attempts = max_rule_retries + 1

        for attempt in range(max_attempts):
            req_headers = headers
            if self._key_rotator is not None:
                req_headers = {**(headers or {}), "X-API-Key": self._key_rotator.current}

            try:
                async with session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=body,
                    headers=req_headers,
                ) as response:
                    if 200 <= response.status < 300:
                        return await self._handle_success(
                            response,
                            response_model,
                        )

                    last_status = response.status

                    if self._retry_policy:
                        rule = self._retry_policy.find_rule(response.status)
                        if rule and attempt < rule.max_retries:
                            delay = rule.delay_for_attempt(attempt)
                            await response.read()
                            if response.status == 429 and self._key_rotator is not None:
                                self._api_key = self._key_rotator.rotate()
                            await asyncio.sleep(delay)
                            continue

                    text = await response.text()
                    content_type = response.headers.get("Content-Type", "")
                    raise_for_status(response.status, text, content_type)

            except ToncenterError:
                raise
            except aiohttp.ClientError as exc:
                last_error = exc
                if attempt < max_attempts - 1:
                    await asyncio.sleep(1.0)
                    continue
                raise ToncenterConnectionError(
                    f"Connection error: {exc}",
                ) from exc

        raise ToncenterRetryError(
            attempts=max_attempts,
            last_status=last_status,
            last_error=last_error,
        )

    async def _handle_success(
        self,
        response: aiohttp.ClientResponse,
        response_model: type[T] | None,
    ) -> t.Any:
        """Process a successful (2xx) response.

        :param response: Aiohttp response.
        :param response_model: Expected return type.
        :return: Parsed result.
        """
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type:
            raise ToncenterError(
                f"HTTP {response.status}: Unexpected HTML response",
            )

        if response_model is None:
            return self._parse_body(await response.text())
        if response_model is bytes:
            return await response.read()
        if response_model is str:
            return await response.text()
        if response_model is bool:
            text = (await response.text()).strip().lower()
            return text in ("true", "1")
        if response_model in (int, float):
            text = await response.text()
            try:
                return response_model(text)  # type: ignore[call-arg]
            except (ValueError, TypeError) as exc:
                raise ToncenterError(
                    f"Cannot parse response as {response_model.__name__}: {text!r}",
                ) from exc

        text = await response.text()
        data = self._parse_body(text)
        if data is None:
            raise ToncenterError(f"Expected JSON response, got: {text}")
        try:
            return _get_adapter(response_model).validate_python(data)
        except ValidationError as exc:
            raise ToncenterValidationError(
                model=response_model,
                errors=exc.errors(),
            ) from exc
