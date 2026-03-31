from __future__ import annotations

import asyncio
import contextlib
import json
import typing as t

import aiohttp

from toncenter.exceptions import (
    ToncenterConnectionLimitError,
    ToncenterError,
    ToncenterStreamingError,
    raise_for_status,
)
from toncenter.streaming.base import StreamingBase
from toncenter.streaming.models import ActionType, ConnectionState, EventType, Finality
from toncenter.types import Network, ReconnectPolicy

_PING_INTERVAL: t.Final[float] = 15.0


class ToncenterWebSocket(StreamingBase):
    """WebSocket streaming transport for TON Center.

    Maintains a WebSocket connection with automatic reconnection
    and periodic ping keepalives (every 15 seconds as recommended
    by the API documentation).

    Unlike SSE, WebSocket supports dynamic subscription management
    after the initial connection via ``dynamic_subscribe()`` and
    ``dynamic_unsubscribe()``.

    An API key is required for streaming connections.
    """

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
        ping_interval: float = _PING_INTERVAL,
        subscribe_timeout: float = 30.0,
    ) -> None:
        super().__init__(
            api_key=api_key,
            network=network,
            base_url=base_url,
            session=session,
            headers=headers,
            reconnect_policy=reconnect_policy,
            on_state_change=on_state_change,
        )
        ws_url = self._base_url.rstrip("/").replace("https://", "wss://").replace("http://", "ws://")
        self._ws_url = f"{ws_url}/api/streaming/v2/ws"
        self._ping_counter = 0
        self._ping_interval = ping_interval
        self._subscribe_timeout = subscribe_timeout
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._msg_counter: int = 0
        self._pending_responses: dict[str, asyncio.Future[dict[str, t.Any]]] = {}

    def _next_id(self) -> str:
        self._msg_counter += 1
        return str(self._msg_counter)

    async def dynamic_subscribe(
        self,
        *,
        addresses: list[str] | None = None,
        trace_external_hash_norms: list[str] | None = None,
        types: list[str | EventType] | None = None,
        min_finality: Finality | str = Finality.FINALIZED,
        include_address_book: bool = False,
        include_metadata: bool = False,
        action_types: list[str | ActionType] | None = None,
        supported_action_types: list[str] | None = None,
    ) -> None:
        """Replace the current subscription (snapshot semantics).

        Can only be called while the WebSocket connection is active
        (i.e. after ``start()`` has established the initial subscription).

        :param addresses: Wallet/contract addresses to monitor, in any form.
        :param trace_external_hash_norms: Trace hashes for trace subscriptions.
        :param types: Event types to receive.
        :param min_finality: Minimum finality level.
        :param include_address_book: Include DNS-resolved names.
        :param include_metadata: Include token metadata.
        :param action_types: Filter actions by type.
        :param supported_action_types: Client-supported action types.
        :raises RuntimeError: If no active WebSocket connection.
        :raises ToncenterStreamingError: If the server rejects the subscription.
        """
        ws = self._require_ws()
        msg_id = self._next_id()

        msg: dict[str, t.Any] = {
            "operation": "subscribe",
            "id": msg_id,
            "min_finality": min_finality.value if isinstance(min_finality, Finality) else min_finality,
            "include_address_book": include_address_book,
            "include_metadata": include_metadata,
        }
        if addresses:
            msg["addresses"] = addresses
        if trace_external_hash_norms:
            msg["trace_external_hash_norms"] = trace_external_hash_norms
        if types:
            msg["types"] = [et.value if hasattr(et, "value") else et for et in types]
        if action_types:
            msg["action_types"] = [a.value if hasattr(a, "value") else a for a in action_types]
        if supported_action_types:
            msg["supported_action_types"] = supported_action_types

        response = await self._send_and_wait(ws, msg, msg_id)
        if response.get("status") != "subscribed":
            error_msg = str(response.get("error", response))
            raise ToncenterStreamingError(f"WebSocket subscribe failed: {error_msg}")

    async def dynamic_unsubscribe(
        self,
        *,
        addresses: list[str] | None = None,
        trace_external_hash_norms: list[str] | None = None,
    ) -> None:
        """Remove addresses or trace hashes from the current subscription.

        :param addresses: Addresses to remove.
        :param trace_external_hash_norms: Trace hashes to remove.
        :raises RuntimeError: If no active WebSocket connection.
        :raises ToncenterStreamingError: If the server rejects the request.
        """
        ws = self._require_ws()
        msg_id = self._next_id()

        msg: dict[str, t.Any] = {
            "operation": "unsubscribe",
            "id": msg_id,
        }
        if addresses:
            msg["addresses"] = addresses
        if trace_external_hash_norms:
            msg["trace_external_hash_norms"] = trace_external_hash_norms

        response = await self._send_and_wait(ws, msg, msg_id)
        if response.get("status") != "unsubscribed":
            error_msg = str(response.get("error", response))
            raise ToncenterStreamingError(f"WebSocket unsubscribe failed: {error_msg}")

    def _require_ws(self) -> aiohttp.ClientWebSocketResponse:
        if self._ws is None or self._ws.closed:
            raise RuntimeError("No active WebSocket connection. Call start() first and wait for the SUBSCRIBED state.")
        return self._ws

    async def _send_and_wait(
        self,
        ws: aiohttp.ClientWebSocketResponse,
        msg: dict[str, t.Any],
        msg_id: str,
    ) -> dict[str, t.Any]:
        """Send a message and wait for the correlated response."""
        future: asyncio.Future[dict[str, t.Any]] = asyncio.get_running_loop().create_future()
        self._pending_responses[msg_id] = future
        try:
            await ws.send_json(msg)
            return await asyncio.wait_for(future, timeout=self._subscribe_timeout)
        except asyncio.CancelledError as err:
            if future.cancelled():
                raise ToncenterStreamingError("WebSocket connection lost while waiting for response") from err
            raise
        finally:
            self._pending_responses.pop(msg_id, None)

    async def _open_stream(
        self,
        params: dict[str, t.Any],
        stop: asyncio.Event | None = None,
    ) -> t.AsyncGenerator[dict[str, t.Any], None]:
        subscribe_msg: dict[str, t.Any] = {
            "operation": "subscribe",
            "id": self._next_id(),
            **params,
        }
        try:
            async with self._session.ws_connect(self._ws_url) as ws:  # type: ignore[union-attr]
                self._ws = ws
                await self._send_subscribe(ws, subscribe_msg)
                await self._set_state(ConnectionState.SUBSCRIBED)

                ping_task = asyncio.create_task(self._ping_loop(ws, stop))
                try:
                    async for data in self._read_messages(ws, stop):
                        yield data
                finally:
                    ping_task.cancel()
                    with contextlib.suppress(asyncio.CancelledError):
                        await ping_task
                    self._ws = None
                    for future in self._pending_responses.values():
                        if not future.done():
                            future.cancel()
                    self._pending_responses.clear()
        except aiohttp.WSServerHandshakeError as exc:
            raise_for_status(
                exc.status,
                exc.message or "",
                "",
            )

    async def _read_messages(
        self,
        ws: aiohttp.ClientWebSocketResponse,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncGenerator[dict[str, t.Any], None]:
        """Read notification messages from the WebSocket, routing control responses to pending futures."""
        while True:
            if stop and stop.is_set():
                return
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                except json.JSONDecodeError as exc:
                    raise ToncenterStreamingError(f"Invalid JSON from WebSocket: {exc}") from exc
                msg_id = data.get("id")
                if msg_id and msg_id in self._pending_responses and "type" not in data:
                    future = self._pending_responses.pop(msg_id)
                    if not future.done():
                        future.set_result(data)
                    continue
                if "type" in data:
                    yield data
            elif msg.type in (
                aiohttp.WSMsgType.CLOSED,
                aiohttp.WSMsgType.ERROR,
                aiohttp.WSMsgType.CLOSING,
            ):
                return

    async def _ping_loop(
        self,
        ws: aiohttp.ClientWebSocketResponse,
        stop: asyncio.Event | None = None,
    ) -> None:
        """Send periodic ping messages to keep the connection alive."""
        while not (stop and stop.is_set()):
            await asyncio.sleep(self._ping_interval)
            if ws.closed:
                return
            self._ping_counter += 1
            try:
                await ws.send_json(
                    {
                        "operation": "ping",
                        "id": f"ping-{self._ping_counter}",
                    }
                )
            except (ConnectionError, aiohttp.ClientError):
                return

    async def _send_subscribe(
        self,
        ws: aiohttp.ClientWebSocketResponse,
        subscribe_msg: dict[str, t.Any],
    ) -> None:
        """Send a subscribe request and validate the response."""
        await ws.send_json(subscribe_msg)

        response = await asyncio.wait_for(ws.receive_json(), timeout=self._subscribe_timeout)
        if response.get("status") != "subscribed":
            error_msg = str(response.get("error", response))
            if "connection limit" in error_msg.lower():
                raise ToncenterConnectionLimitError(error_msg)
            raise ToncenterError(
                f"WebSocket subscribe failed: {error_msg}",
            )
