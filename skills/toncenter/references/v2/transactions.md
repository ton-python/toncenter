# V2 Transactions

7 methods from `client.v2.transactions`:

## get_block_transactions

Get short transaction IDs from a specific block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| workchain | int | yes | — | Workchain ID |
| shard | str | yes | — | Shard ID |
| seqno | int | yes | — | Block sequence number |
| root_hash | str \| None | no | None | Optional root hash for verification |
| file_hash | str \| None | no | None | Optional file hash for verification |
| after_lt | str \| None | no | None | Return transactions after this logical time |
| after_hash | str \| None | no | None | Account hash (hex or base64) to read after |
| count | int \| None | no | None | Maximum number of transactions |

Returns: `BlockTransactions`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 transactions get_block_transactions --workchain 0 --shard -9223372036854775808 --seqno 47000000
```

```python
txs = await client.v2.transactions.get_block_transactions(0, "-9223372036854775808", 47000000, count=10)
```

## get_block_transactions_ext

Get full transaction data from a specific block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| workchain | int | yes | — | Workchain ID |
| shard | str | yes | — | Shard ID |
| seqno | int | yes | — | Block sequence number |
| root_hash | str \| None | no | None | Optional root hash for verification |
| file_hash | str \| None | no | None | Optional file hash for verification |
| after_lt | str \| None | no | None | Return transactions after this logical time |
| after_hash | str \| None | no | None | Account hash (hex or base64) to read after |
| count | int \| None | no | None | Maximum number of transactions |

Returns: `BlockTransactionsExt`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 transactions get_block_transactions_ext --workchain 0 --shard -9223372036854775808 --seqno 47000000
```

```python
txs = await client.v2.transactions.get_block_transactions_ext(0, "-9223372036854775808", 47000000, count=10)
```

## get_transactions

Get transactions for an account address.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| limit | int | no | 10 | Maximum number of transactions |
| lt | str \| None | no | None | Start from this logical time (pagination) |
| hash | str \| None | no | None | Start from this transaction hash (pagination) |
| to_lt | str \| None | no | None | Return transactions up to this logical time |
| archival | bool \| None | no | None | Use archival node for old transactions |

Returns: `list[Transaction]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 transactions get_transactions --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
txs = await client.v2.transactions.get_transactions(
    "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    limit=5,
)
```

## get_transactions_std

Get transactions in a standardized format.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| limit | int | no | 10 | Maximum number of transactions |
| lt | str \| None | no | None | Start from this logical time (pagination) |
| hash | str \| None | no | None | Start from this transaction hash (pagination) |
| to_lt | str \| None | no | None | Return transactions up to this logical time |
| archival | bool \| None | no | None | Use archival node for old transactions |

Returns: `TransactionsStd`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 transactions get_transactions_std --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v2.transactions.get_transactions_std(
    "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    limit=5,
)
```

## try_locate_tx

Locate a transaction by source, destination, and created_lt.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| source | str | yes | — | Source address in any form |
| destination | str | yes | — | Destination address in any form |
| created_lt | str | yes | — | Creation logical time of the message |

Returns: `Transaction`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 transactions try_locate_tx --source 0:... --destination 0:... --created-lt 12345678
```

```python
tx = await client.v2.transactions.try_locate_tx("0:source...", "0:dest...", "12345678")
```

## try_locate_result_tx

Locate the result transaction by source, destination, and created_lt.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| source | str | yes | — | Source address in any form |
| destination | str | yes | — | Destination address in any form |
| created_lt | str | yes | — | Creation logical time of the message |

Returns: `Transaction`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 transactions try_locate_result_tx --source 0:... --destination 0:... --created-lt 12345678
```

```python
tx = await client.v2.transactions.try_locate_result_tx("0:source...", "0:dest...", "12345678")
```

## try_locate_source_tx

Locate the source transaction by source, destination, and created_lt.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| source | str | yes | — | Source address in any form |
| destination | str | yes | — | Destination address in any form |
| created_lt | str | yes | — | Creation logical time of the message |

Returns: `Transaction`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 transactions try_locate_source_tx --source 0:... --destination 0:... --created-lt 12345678
```

```python
tx = await client.v2.transactions.try_locate_source_tx("0:source...", "0:dest...", "12345678")
```
