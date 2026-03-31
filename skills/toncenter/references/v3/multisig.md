# V3 Multisig

2 methods from `client.v3.multisig`:

## get_multisig_orders

Get multisig orders.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] \| None | no | None | Order address in any form (max 1024) |
| multisig_address | list[str] \| None | no | None | Multisig contract address (max 1024) |
| parse_actions | bool | no | False | Parse order actions |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort by last_transaction_lt: "asc" or "desc" |

Returns: `MultisigOrderResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 multisig get_multisig_orders --multisig-address EQ...
```

```python
result = await client.v3.multisig.get_multisig_orders(
    multisig_address=["EQ..."],
    parse_actions=True,
)
```

## get_multisig_wallets

Get multisig wallets.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] \| None | no | None | Multisig contract address in any form (max 1024) |
| wallet_address | list[str] \| None | no | None | Signer or proposer wallet address (max 1024) |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort by last_transaction_lt: "asc" or "desc" |
| include_orders | bool | no | True | Gather multisig orders |

Returns: `MultisigResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 multisig get_multisig_wallets --wallet-address EQ...
```

```python
result = await client.v3.multisig.get_multisig_wallets(
    wallet_address=["EQ..."],
)
```
