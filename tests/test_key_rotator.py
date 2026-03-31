from __future__ import annotations

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

import pytest

from toncenter.client import BaseClient
from toncenter.exceptions import ToncenterTooManyRequestsError
from toncenter.rotator import KeyRotator
from toncenter.types import RetryPolicy, RetryRule


def test_rotate_round_robin() -> None:
    rotator = KeyRotator(["a", "b", "c"])
    assert rotator.current == "a"
    assert rotator.rotate() == "b"
    assert rotator.rotate() == "c"
    assert rotator.rotate() == "a"


def test_single_key_rotate_is_noop() -> None:
    rotator = KeyRotator(["only"])
    assert rotator.rotate() == "only"
    assert rotator.rotate() == "only"


def _make_response(status: int, body: str = "{}") -> MagicMock:
    resp = MagicMock()
    resp.status = status
    resp.headers = {"Content-Type": "application/json"}
    resp.text = AsyncMock(return_value=body)
    resp.read = AsyncMock(return_value=b"")
    return resp


def _mock_session(responses: list[MagicMock]) -> MagicMock:
    """Create a mock session that yields responses in order and records request headers."""
    call_index = 0
    recorded_headers: list[dict[str, str] | None] = []

    @asynccontextmanager
    async def fake_request(**kwargs):  # type: ignore[no-untyped-def]
        nonlocal call_index
        recorded_headers.append(kwargs.get("headers"))
        resp = responses[call_index]
        call_index += 1
        yield resp

    session = MagicMock()
    session.closed = False
    session.request = fake_request
    session._recorded_headers = recorded_headers
    return session


RETRY_429 = RetryPolicy(
    rules=(RetryRule(statuses=frozenset({429}), max_retries=3, base_delay=0.0),),
)


async def test_rotates_key_on_429() -> None:
    """On 429, the next retry uses the rotated key."""
    responses = [
        _make_response(429),
        _make_response(200, '{"ok": true}'),
    ]
    session = _mock_session(responses)

    client = BaseClient(api_key=["key-a", "key-b"], base_url="http://test", retry_policy=RETRY_429)
    client._session = session
    client._is_external_session = True

    await client.request("GET", "/test")

    assert session._recorded_headers[0]["X-API-Key"] == "key-a"
    assert session._recorded_headers[1]["X-API-Key"] == "key-b"


async def test_no_rotation_on_500() -> None:
    """500 retries reuse the same key — rotation is 429-only."""
    retry_500 = RetryPolicy(
        rules=(RetryRule(statuses=frozenset({500}), max_retries=2, base_delay=0.0),),
    )
    responses = [
        _make_response(500),
        _make_response(200, '{"ok": true}'),
    ]
    session = _mock_session(responses)

    client = BaseClient(api_key=["key-a", "key-b"], base_url="http://test", retry_policy=retry_500)
    client._session = session
    client._is_external_session = True

    await client.request("GET", "/test")

    assert session._recorded_headers[0]["X-API-Key"] == "key-a"
    assert session._recorded_headers[1]["X-API-Key"] == "key-a"


async def test_rotation_wraps_through_all_keys() -> None:
    """Keys cycle A→B→C→A when every attempt gets 429."""
    responses = [
        _make_response(429),
        _make_response(429),
        _make_response(429),
        _make_response(200, '{"ok": true}'),
    ]
    session = _mock_session(responses)

    client = BaseClient(api_key=["key-a", "key-b", "key-c"], base_url="http://test", retry_policy=RETRY_429)
    client._session = session
    client._is_external_session = True

    await client.request("GET", "/test")

    keys = [h["X-API-Key"] for h in session._recorded_headers]
    assert keys == ["key-a", "key-b", "key-c", "key-a"]


async def test_rotated_key_persists_to_next_request() -> None:
    """After rotation, the next separate request() call uses the rotated key."""
    responses = [
        _make_response(429),
        _make_response(200, '{"ok": true}'),
        _make_response(200, '{"ok": true}'),
    ]
    session = _mock_session(responses)

    client = BaseClient(api_key=["key-a", "key-b"], base_url="http://test", retry_policy=RETRY_429)
    client._session = session
    client._is_external_session = True

    await client.request("GET", "/first")
    await client.request("GET", "/second")

    keys = [h["X-API-Key"] for h in session._recorded_headers]
    assert keys == ["key-a", "key-b", "key-b"]


async def test_single_key_no_rotator() -> None:
    """String api_key — no rotator created, headers not overridden per-request."""
    responses = [_make_response(200, '{"ok": true}')]
    session = _mock_session(responses)

    client = BaseClient(api_key="single-key", base_url="http://test", retry_policy=RETRY_429)
    client._session = session
    client._is_external_session = True

    assert client._key_rotator is None
    await client.request("GET", "/test")

    assert session._recorded_headers[0] is None


async def test_all_retries_exhausted_raises() -> None:
    """When all keys are rate-limited and retries exhausted, raises 429 error."""
    responses = [
        _make_response(429, '{"error": "rate limited"}'),
        _make_response(429, '{"error": "rate limited"}'),
        _make_response(429, '{"error": "rate limited"}'),
        _make_response(429, '{"error": "rate limited"}'),
    ]
    session = _mock_session(responses)

    client = BaseClient(api_key=["key-a", "key-b"], base_url="http://test", retry_policy=RETRY_429)
    client._session = session
    client._is_external_session = True

    with pytest.raises(ToncenterTooManyRequestsError):
        await client.request("GET", "/test")

    keys = [h["X-API-Key"] for h in session._recorded_headers]
    assert keys == ["key-a", "key-b", "key-a", "key-b"]


async def test_empty_key_list_no_rotator() -> None:
    """Empty list — no rotator, behaves like no api_key."""
    client = BaseClient(api_key=[], base_url="http://test")
    assert client._key_rotator is None
    assert client._api_key == ""
