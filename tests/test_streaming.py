import asyncio

import pytest

from toncenter.streaming.base import StreamingBase
from toncenter.streaming.models import (
    ActionsNotification,
    ConnectionState,
    EventType,
    Finality,
    TraceInvalidatedNotification,
    TransactionsNotification,
)
from toncenter.types import Network

ADDRESS = "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"


class DummyStreaming(StreamingBase):
    """Concrete subclass for unit-testing abstract base."""

    async def _open_stream(self, params, stop=None):
        raise NotImplementedError
        yield  # type: ignore[unreachable]


def _make_client(**kwargs):
    return DummyStreaming("fake-key", Network.MAINNET, **kwargs)


def test_initial_state():
    c = _make_client()
    assert c.state == ConnectionState.IDLE
    assert not c.is_subscribed
    assert not c.is_connecting
    assert not c.is_reconnecting


def test_on_transactions_decorator():
    c = _make_client()

    @c.on_transactions()
    async def handler(n):
        pass

    assert EventType.TRANSACTIONS in c._handlers
    assert len(c._handlers[EventType.TRANSACTIONS]) == 1
    assert c._handlers[EventType.TRANSACTIONS][0].callback is handler


def test_on_transactions_direct():
    c = _make_client()

    async def handler(n):
        pass

    c.on_transactions(handler)

    assert EventType.TRANSACTIONS in c._handlers
    assert c._handlers[EventType.TRANSACTIONS][0].callback is handler


def test_on_actions_with_action_types():
    c = _make_client()

    @c.on_actions(action_types=["ton_transfer", "jetton_transfer"])
    async def handler(n):
        pass

    h = c._handlers[EventType.ACTIONS][0]
    assert h.action_types == ["ton_transfer", "jetton_transfer"]


def test_on_traces():
    c = _make_client()

    @c.on_traces(min_finality=Finality.CONFIRMED)
    async def handler(n):
        pass

    h = c._handlers[EventType.TRACE][0]
    assert h.min_finality == Finality.CONFIRMED


def test_on_account_states_pending_raises():
    c = _make_client()
    with pytest.raises(ValueError, match="confirmed and finalized"):
        c.on_account_states(lambda n: None, min_finality=Finality.PENDING)


def test_on_jettons_pending_raises():
    c = _make_client()
    with pytest.raises(ValueError, match="confirmed and finalized"):
        c.on_jettons(lambda n: None, min_finality=Finality.PENDING)


def test_on_trace_invalidated():
    c = _make_client()

    @c.on_trace_invalidated()
    async def handler(n):
        pass

    assert EventType.TRACE_INVALIDATED in c._handlers


def test_build_subscription_no_handlers():
    c = _make_client()
    with pytest.raises(ValueError, match="No subscribable"):
        c._build_subscription([ADDRESS], None)


def test_build_subscription_no_addresses():
    c = _make_client()
    c.on_transactions(lambda n: None)
    with pytest.raises(ValueError, match="addresses are required"):
        c._build_subscription(None, None)


def test_build_subscription_trace_no_hashes():
    c = _make_client()
    c.on_traces(lambda n: None)
    with pytest.raises(ValueError, match="trace_external_hash_norms are required"):
        c._build_subscription(None, None)


def test_build_subscription_transactions():
    c = _make_client()
    c.on_transactions(lambda n: None, min_finality=Finality.CONFIRMED)

    sub = c._build_subscription([ADDRESS], None)
    assert sub["types"] == [EventType.TRANSACTIONS]
    assert sub["addresses"] == [ADDRESS]
    assert sub["min_finality"] == Finality.CONFIRMED


def test_build_subscription_min_finality_picks_lowest():
    c = _make_client()
    c.on_transactions(lambda n: None, min_finality=Finality.FINALIZED)
    c.on_transactions(lambda n: None, min_finality=Finality.PENDING)

    sub = c._build_subscription([ADDRESS], None)
    assert sub["min_finality"] == Finality.PENDING


def test_build_subscription_merges_action_types():
    c = _make_client()
    c.on_actions(lambda n: None, action_types=["ton_transfer"])
    c.on_actions(lambda n: None, action_types=["jetton_transfer"])

    sub = c._build_subscription([ADDRESS], None)
    assert sorted(sub["action_types"]) == ["jetton_transfer", "ton_transfer"]


async def test_dispatch_finality_filter():
    received = []
    c = _make_client()
    c.on_transactions(lambda n: received.append(n), min_finality=Finality.CONFIRMED)

    pending = TransactionsNotification(
        finality="pending",
        trace_external_hash_norm="abc",
        transactions=[],
    )
    confirmed = TransactionsNotification(
        finality="confirmed",
        trace_external_hash_norm="abc",
        transactions=[],
    )
    finalized = TransactionsNotification(
        finality="finalized",
        trace_external_hash_norm="abc",
        transactions=[],
    )

    await c._dispatch(pending)
    await c._dispatch(confirmed)
    await c._dispatch(finalized)

    assert len(received) == 2
    assert received[0].finality == "confirmed"
    assert received[1].finality == "finalized"


async def test_dispatch_action_type_filter():
    received = []
    c = _make_client()
    c.on_actions(lambda n: received.append(n), action_types=["ton_transfer"])

    match = ActionsNotification(
        finality="finalized",
        trace_external_hash_norm="abc",
        actions=[{"type": "ton_transfer"}],
    )
    no_match = ActionsNotification(
        finality="finalized",
        trace_external_hash_norm="abc",
        actions=[{"type": "jetton_transfer"}],
    )

    await c._dispatch(match)
    await c._dispatch(no_match)

    assert len(received) == 1


async def test_dispatch_async_handler():
    received = []
    c = _make_client()

    async def handler(n):
        received.append(n)

    c.on_transactions(handler)

    notification = TransactionsNotification(
        finality="finalized",
        trace_external_hash_norm="abc",
        transactions=[],
    )
    await c._dispatch(notification)
    assert len(received) == 1


async def test_dispatch_trace_invalidated():
    received = []
    c = _make_client()
    c.on_trace_invalidated(lambda n: received.append(n))

    notification = TraceInvalidatedNotification(trace_external_hash_norm="abc")
    await c._dispatch(notification)
    assert len(received) == 1
    assert received[0].trace_external_hash_norm == "abc"


async def test_set_state_callback_sync():
    states = []
    c = _make_client(on_state_change=lambda s: states.append(s))

    await c._set_state(ConnectionState.CONNECTING)
    await c._set_state(ConnectionState.SUBSCRIBED)

    assert states == [ConnectionState.CONNECTING, ConnectionState.SUBSCRIBED]


async def test_set_state_callback_async():
    states = []

    async def cb(s):
        states.append(s)

    c = _make_client(on_state_change=cb)

    await c._set_state(ConnectionState.CONNECTING)
    assert states == [ConnectionState.CONNECTING]


async def test_set_state_no_duplicate():
    states = []
    c = _make_client(on_state_change=lambda s: states.append(s))

    await c._set_state(ConnectionState.CONNECTING)
    await c._set_state(ConnectionState.CONNECTING)

    assert states == [ConnectionState.CONNECTING]


async def test_wait_subscribed_already():
    c = _make_client()
    await c._set_state(ConnectionState.SUBSCRIBED)
    await c.wait_subscribed(timeout=0.1)


async def test_wait_subscribed_timeout():
    c = _make_client()
    with pytest.raises(asyncio.TimeoutError):
        await c.wait_subscribed(timeout=0.01)


async def test_aenter_raises():
    c = _make_client()
    with pytest.raises(TypeError, match="do not support"):
        async with c:
            pass


async def test_stop_idempotent():
    c = _make_client()
    await c.stop()
    await c.stop()
    assert c.state == ConnectionState.IDLE


async def test_start_already_active():
    c = _make_client()
    c.on_transactions(lambda n: None)
    c._stop = asyncio.Event()
    with pytest.raises(RuntimeError, match="already active"):
        await c.start([ADDRESS])
