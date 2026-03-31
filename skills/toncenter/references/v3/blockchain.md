# V3 Blockchain

10 methods from `client.v3.blockchain`:

## get_adjacent_transactions

Get transactions adjacent to a given transaction by message direction.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| hash | str \| None | no | None | Transaction hash |
| direction | str \| None | no | None | Direction of message |

Returns: `TransactionsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_adjacent_transactions --hash abc123... --direction in
```

```python
result = await client.v3.blockchain.get_adjacent_transactions(hash="abc123...", direction="in")
```

## get_blocks

Get blocks with filtering and pagination.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| workchain | int \| None | no | None | Block workchain |
| shard | str \| None | no | None | Block shard id (use with workchain). Example: 8000000000000000 |
| seqno | int \| None | no | None | Block seqno (use with workchain and shard) |
| root_hash | str \| None | no | None | Block root hash |
| file_hash | str \| None | no | None | Block file hash |
| mc_seqno | int \| None | no | None | Masterchain block seqno |
| start_utime | int \| None | no | None | Blocks generated after given timestamp |
| end_utime | int \| None | no | None | Blocks generated before given timestamp |
| start_lt | int \| None | no | None | Blocks with lt >= start_lt |
| end_lt | int \| None | no | None | Blocks with lt <= end_lt |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort by UTC timestamp: "asc" or "desc" |

Returns: `BlocksResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_blocks --workchain -1 --limit 5
```

```python
result = await client.v3.blockchain.get_blocks(workchain=-1, limit=5)
```

## get_masterchain_block_shard_state

Get shard state for a masterchain block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| seqno | int | yes | — | Masterchain block seqno |

Returns: `BlocksResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_masterchain_block_shard_state --seqno 40000000
```

```python
result = await client.v3.blockchain.get_masterchain_block_shard_state(seqno=40000000)
```

## get_masterchain_block_shards

Get shard blocks for a masterchain block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| seqno | int | yes | — | Masterchain block seqno |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: `BlocksResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_masterchain_block_shards --seqno 40000000
```

```python
result = await client.v3.blockchain.get_masterchain_block_shards(seqno=40000000)
```

## get_masterchain_info

Get first and last masterchain blocks.

(no params)

Returns: `MasterchainInfo`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_masterchain_info
```

```python
info = await client.v3.blockchain.get_masterchain_info()
```

## get_messages

Get messages with filtering and pagination.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| msg_hash | list[str] \| None | no | None | Message hash (hex/base64/base64url) |
| body_hash | str \| None | no | None | Hash of message body |
| source | str \| None | no | None | Source account address. Use "null" for external messages |
| destination | str \| None | no | None | Destination account address. Use "null" for log messages |
| opcode | str \| None | no | None | Opcode in hex or signed 32-bit decimal |
| start_utime | int \| None | no | None | Messages with created_at >= start_utime |
| end_utime | int \| None | no | None | Messages with created_at <= end_utime |
| start_lt | int \| None | no | None | Messages with created_lt >= start_lt |
| end_lt | int \| None | no | None | Messages with created_lt <= end_lt |
| direction | str \| None | no | None | Direction of message |
| exclude_externals | bool \| None | no | None | Exclude external messages |
| only_externals | bool \| None | no | None | Return only external messages |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort by lt: "asc" or "desc" |

Returns: `MessagesResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_messages --source EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v3.blockchain.get_messages(
    source="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    limit=5,
)
```

## get_pending_transactions

Get pending (unfinalized) transactions.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account | list[str] \| None | no | None | List of account addresses (hex/base64/base64url) |
| trace_id | list[str] \| None | no | None | Find transactions by trace id |

Returns: `TransactionsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_pending_transactions --account EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v3.blockchain.get_pending_transactions(
    account=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
)
```

## get_transactions

Get indexed transactions with extensive filtering.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| workchain | int \| None | no | None | Block workchain |
| shard | str \| None | no | None | Block shard id (use with workchain) |
| seqno | int \| None | no | None | Block seqno (use with workchain and shard) |
| mc_seqno | int \| None | no | None | Masterchain block seqno |
| account | list[str] \| None | no | None | List of account addresses |
| exclude_account | list[str] \| None | no | None | Exclude transactions on these accounts |
| hash | str \| None | no | None | Transaction hash |
| lt | int \| None | no | None | Transaction lt |
| start_utime | int \| None | no | None | Transactions after given timestamp |
| end_utime | int \| None | no | None | Transactions before given timestamp |
| start_lt | int \| None | no | None | Transactions with lt >= start_lt |
| end_lt | int \| None | no | None | Transactions with lt <= end_lt |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort by lt: "asc" or "desc" |

Returns: `TransactionsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_transactions --account EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v3.blockchain.get_transactions(
    account=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    limit=5,
)
```

## get_transactions_by_masterchain_block

Get transactions from a specific masterchain block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| seqno | int | yes | — | Masterchain block seqno |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort: "asc" or "desc" |

Returns: `TransactionsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_transactions_by_masterchain_block --seqno 40000000
```

```python
result = await client.v3.blockchain.get_transactions_by_masterchain_block(seqno=40000000)
```

## get_transactions_by_message

Get transactions associated with a message.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| msg_hash | str \| None | no | None | Message hash (hex/base64/base64url) |
| body_hash | str \| None | no | None | Hash of message body |
| opcode | str \| None | no | None | Opcode in hex or signed 32-bit decimal |
| direction | str \| None | no | None | Direction of message |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: `TransactionsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 blockchain get_transactions_by_message --msg-hash abc123...
```

```python
result = await client.v3.blockchain.get_transactions_by_message(msg_hash="abc123...")
```
