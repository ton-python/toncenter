---
name: toncenter
description: >
  Work with TON blockchain via the toncenter Python SDK — query accounts,
  transactions, jettons, NFTs, run smart contract methods, send messages,
  and subscribe to real-time events. Use this skill whenever the user mentions
  TON, toncenter, TON blockchain, wallet balance, jetton transfers, NFT collections,
  smart contract get-methods, or wants to interact with TON in any way. Also use
  when the user works with code that imports from toncenter.rest, toncenter.streaming,
  or toncenter.types, or asks about TON API endpoints, even if they don't explicitly
  mention "toncenter".
---

Python SDK for querying TON blockchain via TON Center API. Covers REST (v2/v3) and streaming (SSE/WebSocket). Read the relevant reference file, then either execute via runner or generate SDK code.

## V2 vs V3

| | V2 | V3 |
|---|---|---|
| Backend | Direct liteserver (tonlib) | Indexed PostgreSQL |
| Latency | Real-time (latest block) | Near real-time (indexer delay) |
| Pagination | No (fixed result sets) | Yes (`limit`, `offset`, `sort`) |
| Jettons/NFTs | `get_token_data` (single item) | Full query API with filters |
| Metadata | Not available | Token metadata, address book, DNS records |
| Traces/Actions | Not available | Full trace trees and parsed actions |
| Best for | Current state, send tx, get-methods | History, search, filters, pagination |

**Use V2 when:** current balance, send transaction, run get-method, block/shard info, fee estimation.

**Use V3 when:** transaction history, jetton/NFT queries, traces/actions, address book, metadata, batch lookups, anything with filters or pagination.

**Both through one client:** `client.v2.accounts.get_address_balance(...)` and `client.v3.jettons.get_jetton_transfers(...)` work in the same session.

**Streaming** — real-time push via SSE (simpler, one-way) or WebSocket (bidirectional, dynamic subscriptions). API key required, free plan allows 2 concurrent connections.

## Routing Table

| User intent | Reference | Runner example |
|---|---|---|
| Installation, setup, first request | `references/quickstart.md` | — |
| SDK version | — | `toncenter -v` |
| Balance, account info, wallet state | `references/v2/accounts.md` | `v2 accounts get_address_balance` |
| Blocks, shards, masterchain | `references/v2/blocks.md` | `v2 blocks get_masterchain_info` |
| Recent transactions (by address, no filters) | `references/v2/transactions.md` | `v2 transactions get_transactions` |
| Send BOC, estimate fee | `references/v2/send.md` | `v2 send estimate_fee` |
| Smart contract get-methods | `references/v2/runmethod.md` | `v2 runmethod run_get_method` |
| Network config params | `references/v2/configuration.md` | `v2 configuration get_config_param` |
| Address format conversion | `references/v2/utils.md` | `v2 utils detect_address` |
| JSON-RPC | `references/v2/rpc.md` | `v2 rpc json_rpc` |
| Account states, metadata, address book | `references/v3/accounts.md` | `v3 accounts get_account_states` |
| Actions, traces (parsed operations) | `references/v3/actions.md` | `v3 actions get_actions` |
| Transactions with filters, pagination, sorting | `references/v3/blockchain.md` | `v3 blockchain get_transactions` |
| Jetton tokens (transfers, wallets, burns) | `references/v3/jettons.md` | `v3 jettons get_jetton_transfers` |
| NFT (collections, items, transfers, sales) | `references/v3/nfts.md` | `v3 nfts get_nft_items` |
| Token metadata (image, name, description) | `references/v3/accounts.md` | `v3 accounts get_metadata` |
| TON DNS records | `references/v3/dns.md` | `v3 dns get_dns_records` |
| Multisig wallets and orders | `references/v3/multisig.md` | `v3 multisig get_multisig_wallets` |
| Vesting contracts | `references/v3/vesting.md` | `v3 vesting get_vesting_contracts` |
| Top accounts, statistics | `references/v3/stats.md` | `v3 stats get_top_accounts_by_balance` |
| Decode opcodes, message bodies | `references/v3/utils.md` | `v3 utils get_decode` |
| V2 methods via V3 endpoint | `references/v3/api_v2.md` | `v3 api_v2 get_address_information` |
| Real-time events (SSE/WebSocket) | `references/streaming.md` | `streaming sse --types transactions` |

## Runner

Always run the runner from the **user's working directory**, not from the skill directory. Use `${CLAUDE_SKILL_DIR}` to reference the script path:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py <api_version> <resource> <method> [--param value ...]
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py streaming <transport> [--param value ...]
```

Requires `toncenter` package installed (`pip install toncenter`).

Configuration priority: CLI flags > environment variables > defaults.

| Source | API Key | Network | Base URL | RPS Limit | RPS Period |
|---|---|---|---|---|---|
| CLI | `--api-key KEY` | `--network mainnet\|testnet` | `--base-url URL` | `--rps-limit N` | `--rps-period N` |
| Env | `TONCENTER_API_KEY` | `TONCENTER_NETWORK` | `TONCENTER_BASE_URL` | `TONCENTER_RPS_LIMIT` | `TONCENTER_RPS_PERIOD` |
| Default | `""` (optional) | `mainnet` | auto by network | `1` | `1.2` |

API key is optional for REST (~1 RPS without key), required for streaming. Get one from @toncenter Telegram bot. Plans: Free (10 RPS, 1 key), Plus (25 RPS, 3 keys), Advanced (100 RPS, 10 keys). Multiple keys on the same plan share a combined RPS limit.

REST — pass `ApiKey` objects with per-key rate limits:

```python
from toncenter.types import ApiKey

ToncenterRestClient(api_key=[ApiKey("free-key", rps_limit=10), ApiKey("plus-key", rps_limit=25)])
```

On 429 (after all retries for current key), rotates to the next key with its own rate limiter.

Streaming — pass a list of key strings for connection limit rotation:

```python
ToncenterWebSocket(["key-1", "key-2"], Network.MAINNET)
```

On connection limit, rotates to next key and reconnects. Single key = fatal error.

Same-plan keys share combined server-side RPS; different-plan keys have independent limits.

## When to Execute vs Generate Code

**Execute via runner** — user wants concrete data ("balance of X", "show NFT Y"), single API call, no complex logic.

**Generate SDK code** — user is building an app, streaming scenarios, multiple calls with conditions, or explicitly asks for code.

## Retries

SDK retries `429` (5 attempts, 0.3s base) and `500, 502, 503, 504` (3 attempts, 0.5s base) with exponential backoff. `542` (liteserver) is NOT retried. With multiple `ApiKey`, 429 exhausts retries for current key then rotates to the next.

## Error Handling

- No API key → works at ~1 RPS; inform user a key from @toncenter unlocks higher limits
- 429 → SDK retries automatically with key rotation if multiple keys provided; if persistent, suggest upgrading plan
- 401 → invalid API key, ask user to check
- 404 → explain meaning (address not found, transaction not found, etc.)
- 542 → liteserver error, not retried; retry manually or try later
- Connection limit → `ToncenterConnectionLimitError` (streaming). Auto-rotates with multiple keys; fatal with single key
- Never guess addresses or parameters — ask the user

## Signing and Sending Transactions

toncenter SDK can send a signed BOC (`send_boc`, `send_boc_return_hash`), but cannot sign transactions — it has no access to private keys.  
For building and signing transactions, recommend `tonutils` (`pip install tonutils`).

## Addresses

- Accept any format (raw, bounceable, non-bounceable) — SDK handles all
- Don't convert addresses without explicit request

## Import Paths

```python
from toncenter.rest import ToncenterRestClient
from toncenter.types import Network, Workchain, ApiKey
from toncenter.streaming import ToncenterSSE, ToncenterWebSocket, Finality, ActionType, EventType, ConnectionState
from toncenter.streaming import TransactionsNotification, ActionsNotification, TraceNotification
from toncenter.streaming import AccountStateNotification, JettonsNotification, TraceInvalidatedNotification
from toncenter.streaming import AccountState, JettonWallet, StreamNotification
from toncenter.utils import raw_to_userfriendly, userfriendly_to_raw, to_nano, to_amount
from toncenter.exceptions import ToncenterError, ToncenterClientError, ToncenterConnectionLimitError, ...
from toncenter.types import RetryPolicy, RetryRule, ReconnectPolicy, DEFAULT_RETRY_POLICY, DEFAULT_RECONNECT_POLICY
```

Never use `from toncenter import ...` — the root package has no re-exports.
