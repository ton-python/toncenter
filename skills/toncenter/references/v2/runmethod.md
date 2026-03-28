# V2 Run Get Method

2 methods from `client.v2.runmethod`:

## run_get_method

Execute a get-method on a smart contract. Stack uses legacy 2-tuple format: `[["num", 42], ["cell", "base64..."]]`.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Smart contract address in any form |
| method | str \| int | yes | — | Method name or numeric ID |
| stack | list[Any] \| None | no | None | Input stack entries in [type, value] format |
| seqno | int \| None | no | None | Masterchain block seqno for historical state |

Returns: ``RunGetMethodResult``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 runmethod run_get_method --address EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs --method get_jetton_data
```

With stack parameter (JSON):
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 runmethod run_get_method --address EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs --method get_wallet_address --stack '[["tvm.Slice", "te6cckEBAQEAJAAAQ4AYOMF/PtnAXVjPKlXzQNBk9Jd9VVq6mz/FBu/6nKwFLBA0Bt8yA=="]]'
```

```python
result = await client.v2.runmethod.run_get_method(
    "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
    "get_jetton_data",
)
```

With stack:
```python
result = await client.v2.runmethod.run_get_method(
    "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
    "get_wallet_address",
    stack=[["tvm.Slice", "te6cckEBAQEAJAAAQ4AYOMF/PtnAXVjPKlXzQNBk9Jd9VVq6mz/FBu/6nKwFLBA0Bt8yA=="]],
)
```

## run_get_method_std

Execute a get-method with standardized TVM stack entries in the response.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Smart contract address in any form |
| method | str \| int | yes | — | Method name or numeric ID |
| stack | list[Any] \| None | no | None | Input TVM stack entries |
| seqno | int \| None | no | None | Masterchain block seqno for historical state |

Returns: ``RunGetMethodStdResult``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 runmethod run_get_method_std --address EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs --method get_jetton_data
```

```python
result = await client.v2.runmethod.run_get_method_std(
    "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
    "get_jetton_data",
)
```
