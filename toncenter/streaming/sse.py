from __future__ import annotations

import asyncio
import codecs
import json
import typing as t

import aiohttp

from toncenter.exceptions import (
    ToncenterStreamingError,
    raise_for_status,
)
from toncenter.streaming.base import StreamingBase
from toncenter.streaming.models import ConnectionState
from toncenter.types import Network, ReconnectPolicy

_HEARTBEAT_TIMEOUT: t.Final[float] = 30.0


class ToncenterSSE(StreamingBase):
    """SSE streaming transport for TON Center.

    Establishes a ``POST`` connection to the SSE endpoint and yields
    parsed notification models as they arrive.  Keepalive comments
    (``:`` lines) are handled transparently; the initial
    ``{"status": "subscribed"}`` acknowledgement is skipped.

    An API key is required for streaming connections.
    """

    def __init__(
        self,
        api_key: str,
        network: Network,
        *,
        base_url: str | None = None,
        session: aiohttp.ClientSession | None = None,
        headers: dict[str, str] | None = None,
        reconnect_policy: ReconnectPolicy | None = None,
        on_state_change: t.Callable[[ConnectionState], t.Any] | None = None,
        heartbeat_timeout: float = _HEARTBEAT_TIMEOUT,
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
        self._heartbeat_timeout = heartbeat_timeout

    async def _open_stream(
        self,
        params: dict[str, t.Any],
        stop: asyncio.Event | None = None,
    ) -> t.AsyncGenerator[dict[str, t.Any], None]:
        url = f"{self._base_url}/api/streaming/v2/sse"
        headers = {"Accept": "text/event-stream"}
        if self._session is None:
            raise RuntimeError("Session not created")
        async with self._session.post(url, json=params, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                content_type = response.headers.get("Content-Type", "")
                raise_for_status(response.status, text, content_type)
            async for data in self._read_notifications(response, stop):
                if "status" in data and "type" not in data:
                    await self._set_state(ConnectionState.SUBSCRIBED)
                    continue
                yield data

    async def _read_notifications(
        self,
        response: aiohttp.ClientResponse,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncGenerator[dict[str, t.Any], None]:
        """Parse SSE text/event-stream into JSON notification dicts.

        :param response: Aiohttp response with ``text/event-stream`` body.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of parsed data dicts.
        :raises ToncenterStreamingError: On heartbeat timeout.
        """
        data_buf = ""

        async for raw_line in _read_lines(response, timeout=self._heartbeat_timeout):
            if stop and stop.is_set():
                return

            line = raw_line.rstrip("\r\n")

            if line.startswith(":"):
                continue

            if not line:
                if data_buf:
                    try:
                        parsed = json.loads(data_buf)
                    except json.JSONDecodeError as exc:
                        raise ToncenterStreamingError(
                            f"Invalid SSE JSON: {data_buf}",
                        ) from exc
                    yield parsed
                data_buf = ""
                continue

            if line.startswith("data:"):
                data_buf += ("\n" if data_buf else "") + line[5:].strip()

        if data_buf:
            try:
                parsed = json.loads(data_buf)
            except json.JSONDecodeError as exc:
                raise ToncenterStreamingError(
                    f"Invalid SSE JSON: {data_buf}",
                ) from exc
            yield parsed


async def _read_lines(
    response: aiohttp.ClientResponse,
    *,
    timeout: float,
) -> t.AsyncGenerator[str, None]:
    """Read lines from a streaming response with heartbeat timeout.

    Uses an incremental UTF-8 decoder to handle multi-byte characters
    that may be split across chunk boundaries.

    :param response: Aiohttp streaming response.
    :param timeout: Seconds to wait before considering the connection dead.
    :return: Async iterator of raw lines.
    :raises ToncenterStreamingError: On heartbeat timeout.
    """
    decoder = codecs.getincrementaldecoder("utf-8")("replace")
    buffer = ""
    while True:
        try:
            chunk = await asyncio.wait_for(
                response.content.read(4096),
                timeout=timeout,
            )
        except asyncio.TimeoutError as err:
            raise ToncenterStreamingError("SSE heartbeat timeout") from err

        if not chunk:
            break

        buffer += decoder.decode(chunk)
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line

    buffer += decoder.decode(b"", final=True)
    if buffer:
        yield buffer
