# 📦 TON Center

[![TON](https://img.shields.io/badge/TON-grey?logo=TON&logoColor=40AEF0)](https://ton.org)
![Python Versions](https://img.shields.io/badge/Python-3.10%20--%203.14-black?color=FFE873&labelColor=3776AB)
[![PyPI](https://img.shields.io/pypi/v/toncenter.svg?color=FFE873&labelColor=3776AB)](https://pypi.python.org/pypi/toncenter)
[![License](https://img.shields.io/github/license/nessshon/toncenter)](https://github.com/nessshon/toncenter/blob/main/LICENSE)
[![Donate](https://img.shields.io/badge/Donate-TON-blue)](https://tonviewer.com/UQCZq3_Vd21-4y4m7Wc-ej9NFOhh_qvdfAkAYAOHoQ__Ness)

![Image](https://raw.githubusercontent.com/nessshon/toncenter/main/banner.png)

![Downloads](https://pepy.tech/badge/toncenter)
![Downloads](https://pepy.tech/badge/toncenter/month)
![Downloads](https://pepy.tech/badge/toncenter/week)

### Python SDK for [TON Center](https://toncenter.com)

Access TON blockchain data via REST API and real-time streaming (SSE & WebSocket).  
API key optional for REST (~1 RPS without key), required for streaming — obtain via [@toncenter](https://t.me/toncenter) bot on Telegram.

> For creating wallets, transferring TON, jettons, etc., use [tonutils](https://github.com/nessshon/tonutils).

**Features**

- **REST API v2** — direct access to TON nodes (accounts, transactions, blocks, smart contracts)
- **REST API v3** — indexed and enriched data (jettons, NFT, DNS, actions, traces)
- **Streaming** — real-time events via SSE and WebSocket

> Support this project — TON: `donate.ness.ton`  
> `UQCZq3_Vd21-4y4m7Wc-ej9NFOhh_qvdfAkAYAOHoQ__Ness`

## Installation

```bash
pip install toncenter
```

[Claude Code](https://claude.ai/code) plugin:
```
/plugin marketplace add nessshon/claude-plugins
/plugin install toncenter@nessshon-plugins
```

## Documentation

[Documentation](https://toncenter.ness.su/) — API reference, guides, and streaming examples.  
[llms.txt](https://toncenter.ness.su/llms.txt) — machine-readable docs for AI tools.

## Examples

**REST API v2**

- [Get account info](https://github.com/nessshon/toncenter/blob/main/examples/rest_v2/get_account_info.py)
- [Get account transactions](https://github.com/nessshon/toncenter/blob/main/examples/rest_v2/get_account_transactions.py)
- [Run get-method](https://github.com/nessshon/toncenter/blob/main/examples/rest_v2/run_get_method.py)
- [Detect address](https://github.com/nessshon/toncenter/blob/main/examples/rest_v2/detect_address.py)
- [Send message](https://github.com/nessshon/toncenter/blob/main/examples/rest_v2/send_message.py)
- [Estimate fee](https://github.com/nessshon/toncenter/blob/main/examples/rest_v2/estimate_fee.py)

**REST API v3**

- [Get account states](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/get_account_states.py)
- [Get jetton wallets](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/get_jetton_wallets.py)
- [Get jetton transfers](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/get_jetton_transfers.py)
- [Get actions](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/get_actions.py)
- [Get NFT items](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/get_nft_items.py)
- [Get transactions](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/get_transactions.py)
- [Get traces](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/get_traces.py)
- [Resolve DNS](https://github.com/nessshon/toncenter/blob/main/examples/rest_v3/resolve_dns.py)

**Streaming** (SSE & WebSocket)

- [SSE streaming](https://github.com/nessshon/toncenter/blob/main/examples/streaming_sse.py)
- [WebSocket streaming](https://github.com/nessshon/toncenter/blob/main/examples/streaming_websocket.py)

## License

This repository is distributed under the [MIT License](https://github.com/nessshon/toncenter/blob/main/LICENSE).
