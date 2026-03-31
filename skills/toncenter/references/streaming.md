# Streaming

Real-time event subscriptions via SSE or WebSocket. Both transports share the decorator-based handler API from `StreamingBase`.

## SSE Constructor

```python
from toncenter.streaming import ToncenterSSE
from toncenter.types import Network

client = ToncenterSSE(
    api_key: str | list[str],
    network: Network,
    *,
    base_url: str | None = None,
    session: aiohttp.ClientSession | None = None,
    headers: dict[str, str] | None = None,
    reconnect_policy: ReconnectPolicy | None = None,
    on_state_change: Callable[[ConnectionState], Any] | None = None,
    heartbeat_timeout: float = 30.0,
)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| api_key | str \| list[str] | — | API key or list of keys for rotation on connection limit |
| network | `Network` | — | `Network.MAINNET` or `Network.TESTNET` |
| base_url | str \| None | None | Custom base URL (overrides network) |
| session | aiohttp.ClientSession \| None | None | External session (not closed by client) |
| headers | dict[str, str] \| None | None | Additional HTTP headers |
| reconnect_policy | `ReconnectPolicy` \| None | None | Custom reconnect policy (default: max 10, 2s delay, 2x backoff) |
| on_state_change | Callable \| None | None | Callback on connection state changes |
| heartbeat_timeout | float | 30.0 | Seconds before considering connection dead |

Connects to `POST {base_url}/api/streaming/v2/sse`.

## WebSocket Constructor

```python
from toncenter.streaming import ToncenterWebSocket
from toncenter.types import Network

client = ToncenterWebSocket(
    api_key: str | list[str],
    network: Network,
    *,
    base_url: str | None = None,
    session: aiohttp.ClientSession | None = None,
    headers: dict[str, str] | None = None,
    reconnect_policy: ReconnectPolicy | None = None,
    on_state_change: Callable[[ConnectionState], Any] | None = None,
    ping_interval: float = 15.0,
    subscribe_timeout: float = 30.0,
)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| api_key | str \| list[str] | — | API key or list of keys for rotation on connection limit |
| network | `Network` | — | `Network.MAINNET` or `Network.TESTNET` |
| base_url | str \| None | None | Custom base URL (overrides network) |
| session | aiohttp.ClientSession \| None | None | External session (not closed by client) |
| headers | dict[str, str] \| None | None | Additional HTTP headers |
| reconnect_policy | `ReconnectPolicy` \| None | None | Custom reconnect policy |
| on_state_change | Callable \| None | None | Callback on connection state changes |
| ping_interval | float | 15.0 | Seconds between ping messages (API recommends 15s) |
| subscribe_timeout | float | 30.0 | Seconds to wait for subscribe response |

Connects to `{base_url}/api/streaming/v2/ws` (converts https:// to wss://).

## start()

Start the transport: create session, subscribe, dispatch notifications to handlers. Blocks until `stop()` is called.

```python
await client.start(
    addresses: list[str] | None = None,
    *,
    trace_external_hash_norms: list[str] | None = None,
    include_address_book: bool = False,
    include_metadata: bool = False,
    supported_action_types: list[str] | None = None,
)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| addresses | list[str] \| None | None | Addresses to monitor (any form) |
| trace_external_hash_norms | list[str] \| None | None | Trace hashes for trace subscriptions |
| include_address_book | bool | False | Include DNS-resolved names in notifications |
| include_metadata | bool | False | Include token metadata in notifications |
| supported_action_types | list[str] \| None | None | Client-supported action types |

## stop()

Stop transport and release resources. Safe to call multiple times.

```python
await client.stop()
```

## Decorator Handlers

Register handlers before calling `start()`. Use as decorators or direct calls.

### on_transactions

```python
@client.on_transactions(min_finality=Finality.FINALIZED)
async def handle(event: TransactionsNotification) -> None:
    for tx in event.transactions:
        print(tx)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| min_finality | `Finality` \| str \| None | None | Minimum finality level filter |

### on_actions

```python
@client.on_actions(min_finality=Finality.FINALIZED, action_types=["jetton_transfer"])
async def handle(event: ActionsNotification) -> None:
    for action in event.actions:
        print(action)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| min_finality | `Finality` \| str \| None | None | Minimum finality level filter |
| action_types | list[str] \| None | None | Filter by action types |

### on_traces

```python
@client.on_traces(min_finality=Finality.FINALIZED)
async def handle(event: TraceNotification) -> None:
    print(event.trace_external_hash_norm)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| min_finality | `Finality` \| str \| None | None | Minimum finality level filter |

### on_account_states

```python
@client.on_account_states()
async def handle(event: AccountStateNotification) -> None:
    print(event.account, event.state)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| min_finality | `Finality` \| str \| None | None | Minimum finality (PENDING not supported, raises ValueError) |

### on_jettons

```python
@client.on_jettons()
async def handle(event: JettonsNotification) -> None:
    print(event.jetton)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| min_finality | `Finality` \| str \| None | None | Minimum finality (PENDING not supported, raises ValueError) |

### on_trace_invalidated

```python
@client.on_trace_invalidated
async def handle(event: TraceInvalidatedNotification) -> None:
    print(event.trace_external_hash_norm)
```

No parameters.

## Finality Levels

| Level | Enum | Description |
|-------|------|-------------|
| Pending | `Finality.PENDING` | Transaction seen but not yet in a block |
| Confirmed | `Finality.CONFIRMED` | In a block but not yet finalized by validators |
| Finalized | `Finality.FINALIZED` | Irreversibly confirmed by validator consensus |

`min_finality` filters: handler receives events at this level and above. E.g., `CONFIRMED` receives confirmed + finalized.

## Notification Models

| Model | Type field | Key fields |
|-------|-----------|------------|
| `TransactionsNotification` | "transactions" | `finality`, `trace_external_hash_norm`, `transactions`, `address_book`, `metadata` |
| `ActionsNotification` | "actions" | `finality`, `trace_external_hash_norm`, `actions`, `address_book`, `metadata` |
| `TraceNotification` | "trace" | `finality`, `trace_external_hash_norm`, `trace`, `transactions`, `actions`, `address_book`, `metadata` |
| `AccountStateNotification` | "account_state_change" | `finality`, `account`, `state` |
| `JettonsNotification` | "jettons_change" | `finality`, `jetton`, `address_book`, `metadata` |
| `TraceInvalidatedNotification` | "trace_invalidated" | `trace_external_hash_norm` |

All notification models with finality have properties: `is_pending`, `is_confirmed`, `is_finalized`.

`StreamNotification` is a union type alias of all notification models.

## Dynamic Subscription (WebSocket Only)

### dynamic_subscribe

Replace the current subscription. Can only be called while WebSocket is active (after `start()`).

```python
await client.dynamic_subscribe(
    *,
    addresses: list[str] | None = None,
    trace_external_hash_norms: list[str] | None = None,
    types: list[str | EventType] | None = None,
    min_finality: Finality | str = Finality.FINALIZED,
    include_address_book: bool = False,
    include_metadata: bool = False,
    action_types: list[str | ActionType] | None = None,
    supported_action_types: list[str] | None = None,
)
```

Raises `RuntimeError` if no active connection. Raises `ToncenterStreamingError` if server rejects.

### dynamic_unsubscribe

Remove addresses or trace hashes from current subscription.

```python
await client.dynamic_unsubscribe(
    *,
    addresses: list[str] | None = None,
    trace_external_hash_norms: list[str] | None = None,
)
```

### wait_subscribed

Wait until connection reaches SUBSCRIBED state.

```python
await client.wait_subscribed(timeout: float | None = None)
```

Raises `asyncio.TimeoutError` if timeout exceeded.

## Connection State

```python
from toncenter.streaming import ConnectionState
```

| State | Value | Description |
|-------|-------|-------------|
| IDLE | "idle" | Not connected |
| CONNECTING | "connecting" | Establishing connection |
| SUBSCRIBED | "subscribed" | Active subscription |
| RECONNECTING | "reconnecting" | Lost connection, attempting reconnect |

Properties: `client.state`, `client.is_subscribed`, `client.is_connecting`, `client.is_reconnecting`.

## ReconnectPolicy

```python
from toncenter.types import ReconnectPolicy

policy = ReconnectPolicy(
    max_reconnects=10,   # max attempts before giving up
    delay=2.0,           # initial delay in seconds
    max_delay=30.0,      # maximum delay
    backoff_factor=2.0,  # exponential backoff multiplier
)
```

Default: `max_reconnects=10, delay=2.0, max_delay=30.0, backoff_factor=2.0`.

## Fatal Errors

These errors stop the connection immediately without reconnect attempts:

- All client errors except 429 (400, 401, 403, 404, 405, 409, 422)
- `ToncenterConnectionLimitError` — connection limit reached. With multiple keys (`list[str]`), auto-rotates to the next key and reconnects. With a single key, fatal.

Only `ToncenterServerError` (5xx), `ToncenterTooManyRequestsError` (429), and `ToncenterStreamingError` trigger automatic reconnection.

After an ungraceful disconnect (crash, killed process) the server may hold ghost sessions for an extended period. Always call `stop()` in a `finally` block.

Multi-key — automatic rotation:

```python
client = ToncenterWebSocket(["key-1", "key-2"], Network.MAINNET)
# On connection limit → rotates to next key automatically
```

Single key — catch manually:

```python
from toncenter.exceptions import ToncenterConnectionLimitError

try:
    await client.start(addresses=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"])
except ToncenterConnectionLimitError:
    print("Connection limit — close other connections or upgrade plan")
finally:
    await client.stop()
```

## Opcode Filtering

The streaming API delivers all transactions for subscribed addresses. Filter by opcode inside the handler:

```python
JETTON_TRANSFER = "0x0f8a7ea5"
JETTON_TRANSFER_NOTIFICATION = "0x7362d09c"

@client.on_transactions(min_finality=Finality.FINALIZED)
async def on_jetton_activity(event: TransactionsNotification) -> None:
    for tx in event.transactions:
        in_msg = tx.get("in_msg", {})
        opcode = in_msg.get("opcode")
        if opcode in (JETTON_TRANSFER, JETTON_TRANSFER_NOTIFICATION):
            print(f"Jetton activity (opcode {opcode}): {tx.get('hash')}")
```

Opcodes are hex strings (e.g. `"0x7362d09c"`).

## Runner Example

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py streaming sse \
    --addresses EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 \
    --types transactions \
    --finality finalized \
    --duration 30

python3 ${CLAUDE_SKILL_DIR}/scripts/run.py streaming ws \
    --addresses EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 \
    --types transactions,actions \
    --finality pending \
    --include-address-book \
    --duration 60
```

Runner streaming params: `--types` (comma-separated event types), `--finality`, `--addresses`, `--trace-hashes`, `--include-address-book`, `--include-metadata`, `--supported-action-types`, `--duration` (seconds, default 60).
