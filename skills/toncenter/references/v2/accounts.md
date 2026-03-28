# V2 Accounts

6 methods from `client.v2.accounts`:

## get_address_information

Get full account information including balance, code, and data.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| seqno | int \| None | no | None | Masterchain block seqno for historical state |

Returns: ``AddressInformation``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 accounts get_address_information --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v2.accounts.get_address_information("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
```

## get_extended_address_information

Get extended account information with detailed account state.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| seqno | int \| None | no | None | Masterchain block seqno for historical state |

Returns: ``ExtendedAddressInformation``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 accounts get_extended_address_information --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v2.accounts.get_extended_address_information("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
```

## get_wallet_information

Get wallet-specific information (type, seqno, wallet_id).

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| seqno | int \| None | no | None | Masterchain block seqno for historical state |

Returns: ``WalletInformation``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 accounts get_wallet_information --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v2.accounts.get_wallet_information("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
```

## get_address_balance

Get account balance in nanotons.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| seqno | int \| None | no | None | Masterchain block seqno for historical state |

Returns: `str`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 accounts get_address_balance --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
balance = await client.v2.accounts.get_address_balance("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
```

## get_address_state

Get account state: "uninitialized", "active", or "frozen".

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| seqno | int \| None | no | None | Masterchain block seqno for historical state |

Returns: `str`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 accounts get_address_state --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
state = await client.v2.accounts.get_address_state("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
```

## get_token_data

Get token contract data (jetton master/wallet, NFT collection/item).

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Token contract address in any form |

Returns: ``TokenData`` (discriminated union: ``JettonMasterData`` | ``JettonWalletData`` | ``NftCollectionData`` | ``NftItemData``)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 accounts get_token_data --address EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs
```

```python
token = await client.v2.accounts.get_token_data("EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs")
```
