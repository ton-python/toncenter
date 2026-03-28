# V3 Vesting

1 method from `client.v3.vesting`:

## get_vesting_contracts

Get vesting contracts.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| contract_address | list[str] \| None | no | None | Vesting contract address in any form (max 1000) |
| wallet_address | list[str] \| None | no | None | Wallet address to filter by owner or sender (max 1000) |
| check_whitelist | bool | no | False | Check if wallet address is in whitelist |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: ``VestingContractsResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 vesting get_vesting_contracts --wallet-address EQ...
```

```python
result = await client.v3.vesting.get_vesting_contracts(
    wallet_address=["EQ..."],
    check_whitelist=True,
)
```
