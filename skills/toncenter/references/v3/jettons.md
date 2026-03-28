# V3 Jettons

4 methods from `client.v3.jettons`:

## get_jetton_burns

Get jetton burn history.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] \| None | no | None | Jetton wallet owner address in any form (max 1000) |
| jetton_wallet | list[str] \| None | no | None | Jetton wallet address in any form (max 1000) |
| jetton_master | str \| None | no | None | Jetton master address in any form |
| start_utime | int \| None | no | None | Transactions after given timestamp |
| end_utime | int \| None | no | None | Transactions before given timestamp |
| start_lt | int \| None | no | None | Transactions with lt >= start_lt |
| end_lt | int \| None | no | None | Transactions with lt <= end_lt |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort: "asc" or "desc" |

Returns: ``JettonBurnsResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 jettons get_jetton_burns --jetton-master EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs --limit 5
```

```python
result = await client.v3.jettons.get_jetton_burns(
    jetton_master="EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
    limit=5,
)
```

## get_jetton_masters

Get jetton master contracts.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] \| None | no | None | Jetton Master address in any form (max 1024) |
| admin_address | list[str] \| None | no | None | Admin address in any form (max 1024) |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: ``JettonMastersResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 jettons get_jetton_masters --address EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs
```

```python
result = await client.v3.jettons.get_jetton_masters(
    address=["EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs"],
)
```

## get_jetton_transfers

Get jetton transfer history.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| owner_address | list[str] \| None | no | None | Jetton wallet owner address in any form (max 1000) |
| jetton_wallet | list[str] \| None | no | None | Jetton wallet address in any form (max 1000) |
| jetton_master | str \| None | no | None | Jetton master address in any form |
| direction | str \| None | no | None | "in" or "out" (only with owner_address) |
| start_utime | int \| None | no | None | Transactions after given timestamp |
| end_utime | int \| None | no | None | Transactions before given timestamp |
| start_lt | int \| None | no | None | Transactions with lt >= start_lt |
| end_lt | int \| None | no | None | Transactions with lt <= end_lt |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort: "asc" or "desc" |

Returns: ``JettonTransfersResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 jettons get_jetton_transfers --jetton-master EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs --limit 5
```

```python
result = await client.v3.jettons.get_jetton_transfers(
    jetton_master="EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
    limit=5,
)
```

## get_jetton_wallets

Get jetton wallet accounts.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] \| None | no | None | Jetton wallet address in any form (max 1000) |
| owner_address | list[str] \| None | no | None | Owner address in any form (max 1000) |
| jetton_address | list[str] \| None | no | None | Jetton Master in any form |
| exclude_zero_balance | bool \| None | no | None | Exclude wallets with 0 balance |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str \| None | no | None | Sort by balance (may be inconsistent during pagination) |

Returns: ``JettonWalletsResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 jettons get_jetton_wallets --owner-address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v3.jettons.get_jetton_wallets(
    owner_address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    exclude_zero_balance=True,
    limit=5,
)
```
