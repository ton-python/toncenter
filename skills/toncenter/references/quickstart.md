# Quickstart

## Installation

```bash
pip install toncenter
```

## Configuration

Environment variables (used by the runner script; all optional for REST):

| Variable | Description | Runner default |
|---|---|---|
| `TONCENTER_API_KEY` | API key (optional for REST, required for streaming) | `""` |
| `TONCENTER_NETWORK` | `"mainnet"` or `"testnet"` | `"mainnet"` |
| `TONCENTER_BASE_URL` | Custom base URL (overrides network) | auto |
| `TONCENTER_RPS_LIMIT` | Rate limit: requests per period | `1` |
| `TONCENTER_RPS_PERIOD` | Rate limit period in seconds | `1.2` |

Note: `ToncenterRestClient` defaults are `rps_limit=0` (disabled) and `rps_period=1.0`. The runner uses its own defaults (1 RPS / 1.2s) to stay within the keyless API limit.

API key is optional for REST (~1 RPS without key). Required for streaming. Get one from @toncenter Telegram bot.

## First REST Request

```python
import asyncio
from toncenter.rest import ToncenterRestClient
from toncenter.types import Network

async def main() -> None:
    async with ToncenterRestClient(network=Network.MAINNET) as client:
        info = await client.v2.accounts.get_address_information(
            "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"
        )
        print(info.model_dump_json(indent=2))

asyncio.run(main())
```

With API key, rate limit, and custom timeout:

```python
async with ToncenterRestClient(
    api_key="your_key",
    network=Network.MAINNET,
    rps_limit=10,
    timeout=30.0,  # seconds, default 10.0
) as client:
    ...
```

With multiple keys and per-key rate limits (rotation on 429):

```python
from toncenter.types import ApiKey

async with ToncenterRestClient(
    api_key=[
        ApiKey("free-key", rps_limit=10),
        ApiKey("plus-key", rps_limit=25),
    ],
    network=Network.MAINNET,
) as client:
    ...
```

## First Streaming Subscription

```python
import asyncio
from toncenter.streaming import Finality, ToncenterSSE, TransactionsNotification
from toncenter.types import Network

client = ToncenterSSE("your_api_key", Network.MAINNET)

@client.on_transactions(min_finality=Finality.FINALIZED)
async def handle_tx(event: TransactionsNotification) -> None:
    for tx in event.transactions:
        print(tx)

async def main() -> None:
    try:
        await client.start(
            addresses=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
        )
    finally:
        await client.stop()

asyncio.run(main())
```

## Custom Endpoint

For self-hosted TON Center instances, pass `base_url`:

```python
async with ToncenterRestClient(
    base_url="https://my-toncenter.example.com",
) as client:
    ...
```

## Utility Functions

```python
from toncenter.utils import raw_to_userfriendly, userfriendly_to_raw, to_nano, to_amount
```

### `raw_to_userfriendly`

Convert raw address (`workchain:hex`) to user-friendly base64 format.

```python
raw_to_userfriendly(
    address: str,
    is_bounceable: bool = False,
    is_url_safe: bool = True,
    is_test_only: bool = False,
) -> str
```

### `userfriendly_to_raw`

Convert user-friendly base64 address to raw format.

```python
userfriendly_to_raw(address: str) -> str
```

Raises `ValueError` on invalid length, CRC, or tag.

### `to_nano`

Convert human-readable amount to smallest units (nanotons).

```python
to_nano(
    value: int | float | str | decimal.Decimal,
    decimals: int = 9,
) -> int
```

Example: `to_nano(1.5)` → `1500000000`

### `to_amount`

Convert smallest units to human-readable `Decimal`.

```python
to_amount(
    value: int,
    decimals: int = 9,
    *,
    precision: int | None = None,
) -> decimal.Decimal
```

Example: `to_amount(1500000000)` → `Decimal('1.5')`

## Error Handling

All SDK exceptions inherit from `ToncenterError`:

- `ToncenterConnectionError` — network-level failures
- `ToncenterClientError` — 4xx HTTP (bad request, unauthorized, not found, rate limit, etc.)
- `ToncenterServerError` — 5xx HTTP (internal error, gateway timeout, liteserver error)
- `ToncenterValidationError` — response didn't match expected Pydantic model
- `ToncenterSessionError` — session not created before request
- `ToncenterConnectionLimitError` — streaming connection limit reached (not retried)
- `ToncenterStreamingError` — streaming transport error
- `ToncenterConnectionLostError` — reconnect limit exhausted during streaming
- `ToncenterRetryError` — all retry attempts exhausted

```python
from toncenter.exceptions import ToncenterError, ToncenterNotFoundError

try:
    result = await client.v2.accounts.get_address_information(address)
except ToncenterNotFoundError:
    print("Address not found")
except ToncenterError as e:
    print(f"API error: {e}")
```
