# V2 Blocks

8 methods from `client.v2.blocks`:

## get_masterchain_info

Get current masterchain block info.

(no params)

Returns: ``MasterchainInfo``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks get_masterchain_info
```

```python
info = await client.v2.blocks.get_masterchain_info()
```

## get_masterchain_block_signatures

Get signatures for a masterchain block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| seqno | int | yes | — | Masterchain block sequence number |

Returns: ``BlockSignatures``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks get_masterchain_block_signatures --seqno 40000000
```

```python
sigs = await client.v2.blocks.get_masterchain_block_signatures(40000000)
```

## get_shard_block_proof

Get proof chain for a shard block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| workchain | int | yes | — | Workchain ID |
| shard | str | yes | — | Shard ID |
| seqno | int | yes | — | Block sequence number |
| from_seqno | int \| None | no | None | Starting masterchain seqno for proof chain |

Returns: ``ShardBlockProof``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks get_shard_block_proof --workchain 0 --shard -9223372036854775808 --seqno 47000000
```

```python
proof = await client.v2.blocks.get_shard_block_proof(0, "-9223372036854775808", 47000000)
```

## get_consensus_block

Get the current consensus block seqno and timestamp.

(no params)

Returns: ``ConsensusBlock``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks get_consensus_block
```

```python
block = await client.v2.blocks.get_consensus_block()
```

## lookup_block

Look up a block by workchain, shard, and one of: seqno, lt, or unixtime.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| workchain | int | yes | — | Workchain ID |
| shard | str | yes | — | Shard ID |
| seqno | int \| None | no | None | Block sequence number |
| lt | str \| None | no | None | Logical time |
| unixtime | int \| None | no | None | UNIX timestamp |

Returns: ``TonBlockIdExt``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks lookup_block --workchain 0 --shard -9223372036854775808 --seqno 47000000
```

```python
block = await client.v2.blocks.lookup_block(0, "-9223372036854775808", seqno=47000000)
```

## get_shards

Get shard blocks for a given masterchain seqno.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| seqno | int | yes | — | Masterchain block sequence number |

Returns: ``Shards``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks get_shards --seqno 40000000
```

```python
shards = await client.v2.blocks.get_shards(40000000)
```

## get_block_header

Get block header information.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| workchain | int | yes | — | Workchain ID |
| shard | str | yes | — | Shard ID |
| seqno | int | yes | — | Block sequence number |
| root_hash | str \| None | no | None | Optional root hash for verification |
| file_hash | str \| None | no | None | Optional file hash for verification |

Returns: ``BlockHeader``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks get_block_header --workchain 0 --shard -9223372036854775808 --seqno 47000000
```

```python
header = await client.v2.blocks.get_block_header(0, "-9223372036854775808", 47000000)
```

## get_out_msg_queue_size

Get outbound message queue sizes for all shards.

(no params)

Returns: ``OutMsgQueueSizes``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 blocks get_out_msg_queue_size
```

```python
sizes = await client.v2.blocks.get_out_msg_queue_size()
```
