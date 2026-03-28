# Claude Code Plugin — TON Center

AI plugin for [Claude Code](https://claude.ai/code) — query TON blockchain through natural language.

## Requirements

- Python 3.10+ with `toncenter` package (`pip install toncenter`)
- API key from [@toncenter](https://t.me/toncenter) bot (optional for REST, required for streaming)

## Installation

In Claude Code:

```
/plugin marketplace add nessshon/claude-plugins
/plugin install toncenter@nessshon-plugins
```

Or test locally:

```bash
claude --plugin-dir /path/to/toncenter
```

## Configuration

Create `.env` in the project root from the template:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `TONCENTER_API_KEY` | API key from [@toncenter](https://t.me/toncenter) bot | none |
| `TONCENTER_NETWORK` | `mainnet` or `testnet` | `mainnet` |
| `TONCENTER_BASE_URL` | Custom base URL (overrides network) | auto |
| `TONCENTER_RPS_LIMIT` | Max requests per period | `1` |
| `TONCENTER_RPS_PERIOD` | Rate limit period in seconds | `1.2` |

## Structure

```
skills/toncenter/
├── SKILL.md              — skill definition and routing table
├── references/
│   ├── quickstart.md          — setup and first request
│   ├── streaming.md           — SSE and WebSocket subscriptions
│   ├── v2/
│   │   ├── accounts.md        — balance, wallet info, token data
│   │   ├── blocks.md          — masterchain, shards, block headers
│   │   ├── transactions.md    — transaction history by address
│   │   ├── send.md            — send BOC, estimate fee
│   │   ├── runmethod.md       — smart contract get-methods
│   │   ├── configuration.md   — network config params
│   │   ├── utils.md           — address format conversion
│   │   └── rpc.md             — JSON-RPC
│   └── v3/
│       ├── accounts.md        — account states, metadata, address book
│       ├── actions.md         — actions, traces
│       ├── blockchain.md      — transactions, messages, blocks (indexed)
│       ├── jettons.md         — transfers, wallets, burns
│       ├── nfts.md            — collections, items, transfers, sales
│       ├── dns.md             — TON DNS records
│       ├── multisig.md        — multisig wallets and orders
│       ├── vesting.md         — vesting contracts
│       ├── stats.md           — top accounts, statistics
│       ├── utils.md           — decode opcodes, message bodies
│       └── api_v2.md          — v2 methods via v3 endpoint
└── scripts/
    └── run.py                 — CLI runner for executing SDK methods
```
