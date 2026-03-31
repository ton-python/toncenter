from __future__ import annotations

import asyncio
import contextlib

import pytest

from tests.conftest import API_KEY, API_KEY_2, NETWORK
from toncenter.exceptions import ToncenterConnectionLimitError
from toncenter.streaming.models import ConnectionState
from toncenter.streaming.sse import ToncenterSSE
from toncenter.streaming.ws import ToncenterWebSocket
from toncenter.types import ReconnectPolicy

TEST_ADDRESS = "EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA"

NO_RECONNECT = ReconnectPolicy(max_reconnects=0)
FAST_RECONNECT = ReconnectPolicy(max_reconnects=2, delay=0.5, max_delay=1.0, backoff_factor=1.0)

pytestmark = pytest.mark.skipif(
    not API_KEY or not API_KEY_2,
    reason="TONCENTER_API_KEY and TONCENTER_API_KEY_2 required",
)


async def _fill_ws_slots(key: str, count: int = 2) -> list[ToncenterWebSocket]:
    """Open `count` WebSocket connections to exhaust the key's connection limit."""
    clients: list[ToncenterWebSocket] = []
    for _ in range(count):
        ws = ToncenterWebSocket(key, NETWORK, reconnect_policy=NO_RECONNECT)

        @ws.on_transactions
        async def _noop(data: object) -> None:
            pass

        await ws.create_session()
        clients.append(ws)
    return clients


async def _cancel_task(task: asyncio.Task[None]) -> None:
    """Cancel a task and suppress errors."""
    if not task.done():
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError, Exception):
            await task


async def _cleanup(
    clients: list[ToncenterWebSocket | ToncenterSSE],
    tasks: list[asyncio.Task[None]],
) -> None:
    """Stop all clients and cancel all tasks."""
    for c in clients:
        with contextlib.suppress(Exception):
            await c.stop()
        with contextlib.suppress(Exception):
            await c.close_session()
    for task in tasks:
        await _cancel_task(task)


class TestWsSingleKeyConnectionLimit:
    async def test_connection_limit_raises_immediately(self) -> None:
        """Exhaust 2 slots on API_KEY, then third connection raises `ToncenterConnectionLimitError`."""
        blockers: list[ToncenterWebSocket] = []
        blocker_tasks: list[asyncio.Task[None]] = []

        try:
            blockers = await _fill_ws_slots(API_KEY, count=2)
            blocker_tasks.extend(asyncio.create_task(ws.start(addresses=[TEST_ADDRESS])) for ws in blockers)

            for ws in blockers:
                await asyncio.wait_for(ws.wait_subscribed(), timeout=15.0)

            assert all(ws.is_subscribed for ws in blockers)

            victim = ToncenterWebSocket(API_KEY, NETWORK, reconnect_policy=NO_RECONNECT)

            @victim.on_transactions
            async def _noop(data: object) -> None:
                pass

            with pytest.raises(ToncenterConnectionLimitError) as exc_info:
                await victim.start(addresses=[TEST_ADDRESS])

            assert "connection limit" in exc_info.value.message.lower()

        finally:
            await _cleanup(blockers, blocker_tasks)


class TestWsMultiKeyRotation:
    async def test_rotates_to_second_key_on_limit(self) -> None:
        """API_KEY has 2 slots filled. Client with [API_KEY, API_KEY_2] rotates to API_KEY_2 and subscribes."""
        blockers: list[ToncenterWebSocket] = []
        blocker_tasks: list[asyncio.Task[None]] = []
        states: list[ConnectionState] = []

        def on_state(state: ConnectionState) -> None:
            states.append(state)

        try:
            blockers = await _fill_ws_slots(API_KEY, count=2)
            blocker_tasks.extend(asyncio.create_task(ws.start(addresses=[TEST_ADDRESS])) for ws in blockers)

            for ws in blockers:
                await asyncio.wait_for(ws.wait_subscribed(), timeout=15.0)

            multi = ToncenterWebSocket(
                [API_KEY, API_KEY_2],
                NETWORK,
                reconnect_policy=FAST_RECONNECT,
                on_state_change=on_state,
            )

            @multi.on_transactions
            async def _noop(data: object) -> None:
                pass

            multi_task = asyncio.create_task(multi.start(addresses=[TEST_ADDRESS]))

            try:
                await asyncio.wait_for(multi.wait_subscribed(), timeout=30.0)
                assert multi.is_subscribed
                assert ConnectionState.RECONNECTING in states
            finally:
                await multi.stop()
                await _cancel_task(multi_task)

        finally:
            await _cleanup(blockers, blocker_tasks)


class TestSseConnectionLimit:
    async def test_single_key_limit_raises(self) -> None:
        """SSE with single key raises `ToncenterConnectionLimitError` on limit."""
        blockers: list[ToncenterWebSocket] = []
        blocker_tasks: list[asyncio.Task[None]] = []

        try:
            blockers = await _fill_ws_slots(API_KEY, count=2)
            blocker_tasks.extend(asyncio.create_task(ws.start(addresses=[TEST_ADDRESS])) for ws in blockers)

            for ws in blockers:
                await asyncio.wait_for(ws.wait_subscribed(), timeout=15.0)

            victim = ToncenterSSE(API_KEY, NETWORK, reconnect_policy=NO_RECONNECT)

            @victim.on_transactions
            async def _noop(data: object) -> None:
                pass

            with pytest.raises(ToncenterConnectionLimitError) as exc_info:
                await victim.start(addresses=[TEST_ADDRESS])

            assert "connection limit" in exc_info.value.message.lower()

        finally:
            await _cleanup(blockers, blocker_tasks)

    async def test_multi_key_rotates(self) -> None:
        """SSE with [API_KEY, API_KEY_2] rotates to API_KEY_2 when API_KEY is at limit."""
        blockers: list[ToncenterWebSocket] = []
        blocker_tasks: list[asyncio.Task[None]] = []

        try:
            blockers = await _fill_ws_slots(API_KEY, count=2)
            blocker_tasks.extend(asyncio.create_task(ws.start(addresses=[TEST_ADDRESS])) for ws in blockers)

            for ws in blockers:
                await asyncio.wait_for(ws.wait_subscribed(), timeout=15.0)

            multi = ToncenterSSE(
                [API_KEY, API_KEY_2],
                NETWORK,
                reconnect_policy=FAST_RECONNECT,
            )

            @multi.on_transactions
            async def _noop(data: object) -> None:
                pass

            multi_task = asyncio.create_task(multi.start(addresses=[TEST_ADDRESS]))

            try:
                await asyncio.wait_for(multi.wait_subscribed(), timeout=30.0)
                assert multi.is_subscribed
            finally:
                await multi.stop()
                await _cancel_task(multi_task)

        finally:
            await _cleanup(blockers, blocker_tasks)
