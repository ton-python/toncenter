# V3 Accounts

4 methods from `client.v3.accounts`:

## get_account_states

Get full account states for multiple addresses.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] | yes | — | List of addresses in any form (max 1000) |
| include_boc | bool | no | True | Include code and data BOCs |

Returns: ``AccountStatesResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 accounts get_account_states --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

Note: for CLI, single address is auto-wrapped into a list by the runner's comma-split logic. For multiple: `--address EQ1...,EQ2...`

```python
result = await client.v3.accounts.get_account_states(
    address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
)
```

## get_address_book

Get address book entries (DNS names, interfaces) for addresses.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] | yes | — | List of addresses in any form (max 1024) |

Returns: ``AddressBook``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 accounts get_address_book --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
book = await client.v3.accounts.get_address_book(
    address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
)
```

## get_metadata

Get address metadata (token info, indexing status).

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] | yes | — | List of addresses in any form (max 1024) |

Returns: ``Metadata``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 accounts get_metadata --address EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs
```

```python
meta = await client.v3.accounts.get_metadata(
    address=["EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs"],
)
```

## get_wallet_states

Get wallet states (balance, seqno, type) for multiple addresses.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] | yes | — | List of addresses in any form (max 1000) |

Returns: ``WalletStatesResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 accounts get_wallet_states --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
wallets = await client.v3.accounts.get_wallet_states(
    address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
)
```
