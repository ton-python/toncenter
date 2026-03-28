# V2 Send

3 methods from `client.v2.send`:

## send_boc

Send a serialized bag-of-cells to the network.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| boc | str | yes | — | Base64-encoded serialized BoC |

Returns: ``ResultOk``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 send send_boc --boc te6cckEBAQEA...
```

```python
result = await client.v2.send.send_boc("te6cckEBAQEA...")
```

## send_boc_return_hash

Send a serialized bag-of-cells and return the message hash.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| boc | str | yes | — | Base64-encoded serialized BoC |

Returns: ``ExtMessageInfo``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 send send_boc_return_hash --boc te6cckEBAQEA...
```

```python
result = await client.v2.send.send_boc_return_hash("te6cckEBAQEA...")
```

## estimate_fee

Estimate transaction fees for a message.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Destination address in any form |
| body | str | yes | — | Base64-encoded message body BoC |
| init_code | str | no | "" | Base64-encoded init code (for deploy) |
| init_data | str | no | "" | Base64-encoded init data (for deploy) |
| ignore_chksig | bool | no | True | Skip signature check |

Returns: ``QueryFees``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 send estimate_fee --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --body te6cckEBAQEA...
```

```python
fees = await client.v2.send.estimate_fee(
    "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    "te6cckEBAQEA...",
    ignore_chksig=True,
)
```
