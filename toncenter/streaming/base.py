from __future__ import annotations

import abc
import asyncio
import inspect
import typing as t
from dataclasses import dataclass

import aiohttp

from toncenter.client import BaseClient
from toncenter.exceptions import (
    STREAMING_RECOVERABLE,
    ToncenterConnectionLimitError,
    ToncenterConnectionLostError,
    ToncenterError,
)
from toncenter.streaming.models import (
    NOTIFICATION_MODEL_MAP,
    ActionsNotification,
    ConnectionState,
    EventType,
    Finality,
    StreamNotification,
    _FinalityMixin,
)
from toncenter.streaming.rotator import StreamingKeyRotator
from toncenter.types import (
    DEFAULT_RECONNECT_POLICY,
    NETWORK_BASE_URLS,
    Network,
    ReconnectPolicy,
)

_F = t.TypeVar("_F", bound=t.Callable[..., t.Any])

_FINALITY_ORDER: t.Final[dict[str, int]] = {
    "pending": 0,
    "confirmed": 1,
    "finalized": 2,
}

_SUBSCRIBABLE: t.Final[frozenset[str]] = frozenset(
    {
        EventType.TRANSACTIONS,
        EventType.ACTIONS,
        EventType.TRACE,
        EventType.ACCOUNT_STATE_CHANGE,
        EventType.JETTONS_CHANGE,
    }
)


@dataclass(slots=True)
class _Handler:
    callback: t.Callable[..., t.Any]
    min_finality: Finality | None = None
    action_types: list[str] | None = None


class StreamingBase(BaseClient, abc.ABC):
    """Abstract base for streaming transports (SSE / WebSocket)."""

    def __init__(
        self,
        api_key: str | list[str],
        network: Network,
        *,
        base_url: str | None = None,
        session: aiohttp.ClientSession | None = None,
        headers: dict[str, str] | None = None,
        reconnect_policy: ReconnectPolicy | None = None,
        on_state_change: t.Callable[[ConnectionState], t.Any] | None = None,
    ) -> None:
        if isinstance(api_key, list):
            self._streaming_rotator: StreamingKeyRotator | None = StreamingKeyRotator(api_key) if api_key else None
            initial_key = api_key[0] if api_key else ""
        else:
            self._streaming_rotator = None
            initial_key = api_key

        super().__init__(
            api_key=initial_key,
            base_url=base_url or NETWORK_BASE_URLS[network],
            session=session,
            headers=headers,
            timeout=0.0,
            retry_policy=None,
        )
        self._reconnect_policy = reconnect_policy or DEFAULT_RECONNECT_POLICY
        self._on_state_change = on_state_change
        self._handlers: dict[str, list[_Handler]] = {}
        self._stop: asyncio.Event | None = None
        self._state: ConnectionState = ConnectionState.IDLE
        self._subscribed_event = asyncio.Event()

    @property
    def state(self) -> ConnectionState:
        """Current connection state."""
        return self._state

    @property
    def is_subscribed(self) -> bool:
        """``True`` if currently subscribed and receiving notifications."""
        return self._state == ConnectionState.SUBSCRIBED

    @property
    def is_connecting(self) -> bool:
        """``True`` if establishing initial connection."""
        return self._state == ConnectionState.CONNECTING

    @property
    def is_reconnecting(self) -> bool:
        """``True`` if reconnecting after a connection loss."""
        return self._state == ConnectionState.RECONNECTING

    async def wait_subscribed(self, timeout: float | None = None) -> None:
        """Wait until the transport reaches ``SUBSCRIBED`` state.

        :param timeout: Maximum seconds to wait, or ``None`` for no limit.
        :raises asyncio.TimeoutError: If *timeout* is reached before subscribing.
        """
        if self._state == ConnectionState.SUBSCRIBED:
            return
        await asyncio.wait_for(self._subscribed_event.wait(), timeout=timeout)

    async def _set_state(self, new: ConnectionState) -> None:
        if self._state == new:
            return
        if self._state == ConnectionState.SUBSCRIBED:
            self._subscribed_event.clear()
        self._state = new
        if new == ConnectionState.SUBSCRIBED:
            self._subscribed_event.set()
        if self._on_state_change is not None:
            result = self._on_state_change(new)
            if inspect.isawaitable(result):
                await result

    @t.overload
    def _register(
        self,
        notification_type: str,
        callback: _F,
        *,
        min_finality: Finality | str | None = ...,
        action_types: list[str] | None = ...,
    ) -> _F: ...

    @t.overload
    def _register(
        self,
        notification_type: str,
        callback: None = ...,
        *,
        min_finality: Finality | str | None = ...,
        action_types: list[str] | None = ...,
    ) -> t.Callable[[_F], _F]: ...

    def _register(
        self,
        notification_type: str,
        callback: _F | None = None,
        *,
        min_finality: Finality | str | None = None,
        action_types: list[str] | None = None,
    ) -> _F | t.Callable[[_F], _F]:
        def decorator(fn: _F) -> _F:
            parsed = Finality(min_finality) if isinstance(min_finality, str) else min_finality
            self._handlers.setdefault(notification_type, []).append(
                _Handler(
                    callback=fn,
                    min_finality=parsed,
                    action_types=(
                        [a.value if hasattr(a, "value") else a for a in action_types] if action_types else None
                    ),
                ),
            )
            return fn

        return decorator(callback) if callback is not None else decorator

    @t.overload
    def on_transactions(self, callback: _F, *, min_finality: Finality | str | None = ...) -> _F: ...

    @t.overload
    def on_transactions(
        self, callback: None = ..., *, min_finality: Finality | str | None = ...
    ) -> t.Callable[[_F], _F]: ...

    def on_transactions(
        self,
        callback: _F | None = None,
        *,
        min_finality: Finality | str | None = None,
    ) -> _F | t.Callable[[_F], _F]:
        """Register a handler for ``transactions`` notifications."""
        return self._register(EventType.TRANSACTIONS, callback, min_finality=min_finality)

    @t.overload
    def on_actions(
        self, callback: _F, *, min_finality: Finality | str | None = ..., action_types: list[str] | None = ...
    ) -> _F: ...

    @t.overload
    def on_actions(
        self, callback: None = ..., *, min_finality: Finality | str | None = ..., action_types: list[str] | None = ...
    ) -> t.Callable[[_F], _F]: ...

    def on_actions(
        self,
        callback: _F | None = None,
        *,
        min_finality: Finality | str | None = None,
        action_types: list[str] | None = None,
    ) -> _F | t.Callable[[_F], _F]:
        """Register a handler for ``actions`` notifications."""
        return self._register(
            EventType.ACTIONS,
            callback,
            min_finality=min_finality,
            action_types=action_types,
        )

    @t.overload
    def on_traces(self, callback: _F, *, min_finality: Finality | str | None = ...) -> _F: ...

    @t.overload
    def on_traces(self, callback: None = ..., *, min_finality: Finality | str | None = ...) -> t.Callable[[_F], _F]: ...

    def on_traces(
        self,
        callback: _F | None = None,
        *,
        min_finality: Finality | str | None = None,
    ) -> _F | t.Callable[[_F], _F]:
        """Register a handler for ``trace`` notifications."""
        return self._register(EventType.TRACE, callback, min_finality=min_finality)

    @t.overload
    def on_account_states(self, callback: _F, *, min_finality: Finality | str | None = ...) -> _F: ...

    @t.overload
    def on_account_states(
        self, callback: None = ..., *, min_finality: Finality | str | None = ...
    ) -> t.Callable[[_F], _F]: ...

    def on_account_states(
        self,
        callback: _F | None = None,
        *,
        min_finality: Finality | str | None = None,
    ) -> _F | t.Callable[[_F], _F]:
        """Register a handler for ``account_state_change`` notifications."""
        if min_finality is not None:
            raw = min_finality.value if isinstance(min_finality, Finality) else min_finality
            if raw == Finality.PENDING:
                raise ValueError(
                    "account_state_change events are only emitted at confirmed and finalized finality levels"
                )
        return self._register(EventType.ACCOUNT_STATE_CHANGE, callback, min_finality=min_finality)

    @t.overload
    def on_jettons(self, callback: _F, *, min_finality: Finality | str | None = ...) -> _F: ...

    @t.overload
    def on_jettons(
        self, callback: None = ..., *, min_finality: Finality | str | None = ...
    ) -> t.Callable[[_F], _F]: ...

    def on_jettons(
        self,
        callback: _F | None = None,
        *,
        min_finality: Finality | str | None = None,
    ) -> _F | t.Callable[[_F], _F]:
        """Register a handler for ``jettons_change`` notifications."""
        if min_finality is not None:
            raw = min_finality.value if isinstance(min_finality, Finality) else min_finality
            if raw == Finality.PENDING:
                raise ValueError("jettons_change events are only emitted at confirmed and finalized finality levels")
        return self._register(EventType.JETTONS_CHANGE, callback, min_finality=min_finality)

    @t.overload
    def on_trace_invalidated(self, callback: _F) -> _F: ...

    @t.overload
    def on_trace_invalidated(self, callback: None = ...) -> t.Callable[[_F], _F]: ...

    def on_trace_invalidated(
        self,
        callback: _F | None = None,
    ) -> _F | t.Callable[[_F], _F]:
        """Register a handler for ``trace_invalidated`` notifications."""
        return self._register(EventType.TRACE_INVALIDATED, callback)

    def _build_subscription(
        self,
        addresses: list[str] | None,
        trace_external_hash_norms: list[str] | None,
    ) -> dict[str, t.Any]:
        types = sorted(k for k in self._handlers if k in _SUBSCRIBABLE)
        if not types:
            raise ValueError("No subscribable notification handlers registered")

        fin = Finality.FINALIZED
        for handlers in self._handlers.values():
            for h in handlers:
                if h.min_finality is not None and _FINALITY_ORDER[h.min_finality] < _FINALITY_ORDER[fin]:
                    fin = h.min_finality

        action_types: list[str] | None = None
        ah = self._handlers.get(EventType.ACTIONS, [])
        if ah and all(h.action_types is not None for h in ah):
            merged = {at for h in ah for at in (h.action_types or [])}
            action_types = sorted(merged) if merged else None

        non_trace = [et for et in types if et != EventType.TRACE]
        if non_trace and not addresses:
            raise ValueError(
                f"addresses are required for event types: {non_trace}. Only 'trace' subscriptions can omit addresses.",
            )
        if EventType.TRACE in types and not trace_external_hash_norms:
            raise ValueError("trace_external_hash_norms are required for trace subscriptions")

        result: dict[str, t.Any] = {"types": types, "min_finality": fin}
        if addresses:
            result["addresses"] = addresses
        if trace_external_hash_norms:
            result["trace_external_hash_norms"] = trace_external_hash_norms
        if action_types:
            result["action_types"] = action_types
        return result

    async def _dispatch(self, notification: StreamNotification) -> None:
        for handler in self._handlers.get(notification.type, []):
            if handler.min_finality is not None and isinstance(notification, _FinalityMixin):
                n_order = _FINALITY_ORDER.get(getattr(notification, "finality", ""), -1)
                if n_order < 0:
                    continue
                h_order = _FINALITY_ORDER.get(handler.min_finality.value, 0)
                if n_order < h_order:
                    continue

            if isinstance(notification, ActionsNotification) and handler.action_types is not None:
                wanted = set(handler.action_types)
                if not any(a.get("type") in wanted for a in notification.actions):
                    continue

            result = handler.callback(notification)
            if inspect.isawaitable(result):
                await result

    async def subscribe(
        self,
        *,
        addresses: list[str] | None = None,
        trace_external_hash_norms: list[str] | None = None,
        types: list[str] | None = None,
        min_finality: Finality | str = Finality.FINALIZED,
        include_address_book: bool = False,
        include_metadata: bool = False,
        action_types: list[str] | None = None,
        supported_action_types: list[str] | None = None,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncGenerator[StreamNotification, None]:
        """Low-level subscription generator.

        Opens one connection, yields typed notifications. Reconnects automatically.
        For high-level usage prefer ``on_*()`` decorators + ``start()``.
        """
        non_trace = [et for et in (types or []) if et != "trace"]
        if non_trace and not addresses:
            raise ValueError(
                f"addresses are required for event types: {non_trace}. Only 'trace' subscriptions can omit addresses.",
            )

        params: dict[str, t.Any] = {
            "min_finality": min_finality.value if isinstance(min_finality, Finality) else min_finality,
            "include_address_book": include_address_book,
            "include_metadata": include_metadata,
        }
        if addresses:
            params["addresses"] = addresses
        if trace_external_hash_norms:
            params["trace_external_hash_norms"] = trace_external_hash_norms
        if types:
            params["types"] = [et.value if hasattr(et, "value") else et for et in types]
        if action_types:
            params["action_types"] = [a.value if hasattr(a, "value") else a for a in action_types]
        if supported_action_types:
            params["supported_action_types"] = supported_action_types

        async for data in self._stream_with_reconnect(params, stop):
            model = NOTIFICATION_MODEL_MAP.get(data.get("type", ""))
            if model is not None:
                yield model.model_validate(data)  # type: ignore[misc]

    async def _stream_with_reconnect(
        self,
        params: dict[str, t.Any],
        stop: asyncio.Event | None = None,
    ) -> t.AsyncGenerator[dict[str, t.Any], None]:
        attempt = 0
        await self._set_state(ConnectionState.CONNECTING)

        while not (stop and stop.is_set()):
            try:
                async for data in self._open_stream(params, stop):
                    attempt = 0
                    yield data
            except ToncenterConnectionLimitError:
                if self._streaming_rotator is not None and len(self._streaming_rotator) > 1:
                    self._api_key = self._streaming_rotator.rotate()
                    await self.close_session()
                    await self.create_session()
                else:
                    await self._set_state(ConnectionState.IDLE)
                    raise
            except ToncenterError as exc:
                if not isinstance(exc, STREAMING_RECOVERABLE):
                    await self._set_state(ConnectionState.IDLE)
                    raise
            except (aiohttp.ClientError, OSError):
                pass

            if stop and stop.is_set():
                await self._set_state(ConnectionState.IDLE)
                return

            attempt += 1
            if self._reconnect_policy.max_reconnects != -1 and attempt > self._reconnect_policy.max_reconnects:
                await self._set_state(ConnectionState.IDLE)
                raise ToncenterConnectionLostError(attempts=attempt)

            await self._set_state(ConnectionState.RECONNECTING)
            await asyncio.sleep(self._reconnect_policy.delay_for_attempt(attempt - 1))

    @abc.abstractmethod
    async def _open_stream(
        self,
        params: dict[str, t.Any],
        stop: asyncio.Event | None = None,
    ) -> t.AsyncGenerator[dict[str, t.Any], None]:
        """Open a transport-specific streaming connection and yield raw notification dicts."""
        raise NotImplementedError
        yield  # type: ignore[unreachable]

    async def start(
        self,
        addresses: list[str] | None = None,
        *,
        trace_external_hash_norms: list[str] | None = None,
        include_address_book: bool = False,
        include_metadata: bool = False,
        supported_action_types: list[str] | None = None,
    ) -> None:
        """Start the streaming transport: create session, subscribe, and dispatch.

        Blocks until ``stop()`` is called or a fatal error occurs.
        Creates an internal aiohttp session on entry and closes it on exit
        (unless an external session was provided via the constructor).

        :param addresses: Wallet/contract addresses to monitor, in any form.
        :param trace_external_hash_norms: Trace hashes for trace subscriptions.
        :param include_address_book: Include DNS-resolved names in notifications.
        :param include_metadata: Include token metadata in notifications.
        :param supported_action_types: Advertise client-supported action types.
        """
        if self._stop is not None:
            raise RuntimeError("start() is already active")

        sub = self._build_subscription(addresses, trace_external_hash_norms)
        self._stop = asyncio.Event()
        await self.create_session()
        try:
            async for notification in self.subscribe(
                addresses=sub.get("addresses"),
                trace_external_hash_norms=sub.get("trace_external_hash_norms"),
                types=sub.get("types"),
                min_finality=sub["min_finality"],
                action_types=sub.get("action_types"),
                include_address_book=include_address_book,
                include_metadata=include_metadata,
                supported_action_types=supported_action_types,
                stop=self._stop,
            ):
                await self._dispatch(notification)
        finally:
            self._stop = None
            await self.close_session()

    async def stop(self) -> None:
        """Stop the streaming transport and release resources.

        Signals the dispatch loop to exit, closes the aiohttp session
        (unless externally provided), and resets the connection state.
        Safe to call multiple times.
        """
        if self._stop is not None:
            self._stop.set()
        await self.close_session()
        await self._set_state(ConnectionState.IDLE)

    async def __aenter__(self) -> t.NoReturn:
        raise TypeError("Streaming transports do not support 'async with'. Use start() and stop() instead.")

    async def __aexit__(self, *args: t.Any) -> None:
        pass
