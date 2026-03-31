from __future__ import annotations

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

import pytest

from toncenter.exceptions import ToncenterTooManyRequestsError
from toncenter.rest.client import ToncenterRestClient
from toncenter.rest.rotator import KeyRotator
from toncenter.streaming.rotator import StreamingKeyRotator
from toncenter.types import ApiKey, RetryPolicy, RetryRule


class TestKeyRotator:
    def test_round_robin(self) -> None:
        rotator = KeyRotator([ApiKey("a"), ApiKey("b"), ApiKey("c")])
        assert rotator.current_key == "a"
        assert rotator.rotate() == "b"
        assert rotator.rotate() == "c"
        assert rotator.rotate() == "a"

    def test_single_key_noop(self) -> None:
        rotator = KeyRotator([ApiKey("only")])
        assert rotator.rotate() == "only"
        assert rotator.rotate() == "only"

    def test_limiter_created_when_rps_positive(self) -> None:
        rotator = KeyRotator([ApiKey("a", rps_limit=10), ApiKey("b")])
        assert rotator.current_limiter is not None
        rotator.rotate()
        assert rotator.current_limiter is None

    def test_len(self) -> None:
        rotator = KeyRotator([ApiKey("a"), ApiKey("b")])
        assert len(rotator) == 2

    def test_api_key_defaults(self) -> None:
        k = ApiKey("test")
        assert k.rps_limit == 0
        assert k.rps_period == 1.0


class TestStreamingKeyRotator:
    def test_round_robin(self) -> None:
        rotator = StreamingKeyRotator(["a", "b", "c"])
        assert rotator.current == "a"
        assert rotator.rotate() == "b"
        assert rotator.rotate() == "c"
        assert rotator.rotate() == "a"

    def test_single_key_noop(self) -> None:
        rotator = StreamingKeyRotator(["only"])
        assert rotator.rotate() == "only"

    def test_len(self) -> None:
        rotator = StreamingKeyRotator(["a", "b"])
        assert len(rotator) == 2


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


class TestRestClientSingleKey:
    async def test_string_key_backward_compat(self) -> None:
        """String api_key — no rotator, works as before."""
        responses = [_make_response(200, '{"ok": true}')]
        session = _mock_session(responses)

        client = ToncenterRestClient(api_key="single-key", base_url="http://test", retry_policy=RETRY_429)
        client._session = session
        client._is_external_session = True

        assert client._key_rotator is None
        await client.request("GET", "/test")
        assert session._recorded_headers[0] is None

    async def test_string_key_with_rps_limit(self) -> None:
        """String api_key + rps_limit creates a rate limiter."""
        client = ToncenterRestClient(api_key="key", rps_limit=10)
        assert client._rate_limiter is not None
        assert client._key_rotator is None

    async def test_apikey_single(self) -> None:
        """Single ApiKey — limiter from ApiKey, constructor rps_limit ignored."""
        client = ToncenterRestClient(api_key=ApiKey("key", rps_limit=10), rps_limit=99)
        assert client._rate_limiter is not None
        assert client._key_rotator is None

    async def test_empty_list_no_rotator(self) -> None:
        """Empty list — no rotator, no key."""
        client = ToncenterRestClient(api_key=[])
        assert client._key_rotator is None
        assert client._api_key == ""


class TestRestClientMultiKey:
    async def test_rotates_on_429(self) -> None:
        """First key 429 exhausted → rotates to second key, succeeds."""
        responses = [
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(200, '{"ok": true}'),
        ]
        session = _mock_session(responses)

        client = ToncenterRestClient(
            api_key=[ApiKey("key-a"), ApiKey("key-b")],
            base_url="http://test",
            retry_policy=RETRY_429,
        )
        client._session = session
        client._is_external_session = True

        await client.request("GET", "/test")

        keys = [h["X-API-Key"] for h in session._recorded_headers]
        assert keys[0] == "key-a"
        assert keys[-1] == "key-b"

    async def test_all_keys_exhausted_raises(self) -> None:
        """Both keys 429 exhausted → raises ToncenterTooManyRequestsError."""
        responses = [_make_response(429, '{"error": "rate limited"}') for _ in range(8)]
        session = _mock_session(responses)

        client = ToncenterRestClient(
            api_key=[ApiKey("key-a"), ApiKey("key-b")],
            base_url="http://test",
            retry_policy=RETRY_429,
        )
        client._session = session
        client._is_external_session = True

        with pytest.raises(ToncenterTooManyRequestsError):
            await client.request("GET", "/test")

    async def test_per_request_header_matches_current_key(self) -> None:
        """X-API-Key header matches the current rotator key."""
        responses = [_make_response(200, '{"ok": true}')]
        session = _mock_session(responses)

        client = ToncenterRestClient(
            api_key=[ApiKey("key-a"), ApiKey("key-b")],
            base_url="http://test",
            retry_policy=RETRY_429,
        )
        client._session = session
        client._is_external_session = True

        await client.request("GET", "/test")
        assert session._recorded_headers[0]["X-API-Key"] == "key-a"

    async def test_rotated_key_persists_to_next_request(self) -> None:
        """After rotation, the next request() call starts from the rotated key."""
        responses = [
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(200, '{"ok": true}'),
            _make_response(200, '{"ok": true}'),
        ]
        session = _mock_session(responses)

        client = ToncenterRestClient(
            api_key=[ApiKey("key-a"), ApiKey("key-b")],
            base_url="http://test",
            retry_policy=RETRY_429,
        )
        client._session = session
        client._is_external_session = True

        await client.request("GET", "/first")
        await client.request("GET", "/second")

        keys = [h["X-API-Key"] for h in session._recorded_headers]
        assert keys[-1] == "key-b", "Second request should start from rotated key"

    async def test_wrap_around_through_all_keys(self) -> None:
        """Keys cycle A→B→C when each key's retries are exhausted on 429."""
        retry_1 = RetryPolicy(
            rules=(RetryRule(statuses=frozenset({429}), max_retries=1, base_delay=0.0),),
        )
        responses = [
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(429, '{"error": "rate limited"}'),
            _make_response(200, '{"ok": true}'),
        ]
        session = _mock_session(responses)

        client = ToncenterRestClient(
            api_key=[ApiKey("key-a"), ApiKey("key-b"), ApiKey("key-c")],
            base_url="http://test",
            retry_policy=retry_1,
        )
        client._session = session
        client._is_external_session = True

        await client.request("GET", "/test")

        keys = [h["X-API-Key"] for h in session._recorded_headers]
        assert keys == ["key-a", "key-a", "key-b", "key-b", "key-c"]

    async def test_all_keys_exhausted_tries_each_key(self) -> None:
        """All keys get a full retry cycle before raising."""
        retry_1 = RetryPolicy(
            rules=(RetryRule(statuses=frozenset({429}), max_retries=1, base_delay=0.0),),
        )
        responses = [_make_response(429, '{"error": "rate limited"}') for _ in range(6)]
        session = _mock_session(responses)

        client = ToncenterRestClient(
            api_key=[ApiKey("key-a"), ApiKey("key-b"), ApiKey("key-c")],
            base_url="http://test",
            retry_policy=retry_1,
        )
        client._session = session
        client._is_external_session = True

        with pytest.raises(ToncenterTooManyRequestsError):
            await client.request("GET", "/test")

        keys = [h["X-API-Key"] for h in session._recorded_headers]
        assert keys == ["key-a", "key-a", "key-b", "key-b", "key-c", "key-c"]

    async def test_no_rotation_on_500(self) -> None:
        """500 retries reuse the same key — rotation is 429-only."""
        retry_500 = RetryPolicy(
            rules=(RetryRule(statuses=frozenset({500}), max_retries=2, base_delay=0.0),),
        )
        responses = [
            _make_response(500),
            _make_response(200, '{"ok": true}'),
        ]
        session = _mock_session(responses)

        client = ToncenterRestClient(
            api_key=[ApiKey("key-a"), ApiKey("key-b")],
            base_url="http://test",
            retry_policy=retry_500,
        )
        client._session = session
        client._is_external_session = True

        await client.request("GET", "/test")

        keys = [h["X-API-Key"] for h in session._recorded_headers]
        assert keys == ["key-a", "key-a"]
