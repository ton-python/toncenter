# V2 JSON-RPC

1 method from `client.v2.rpc`:

## json_rpc

Execute a raw JSON-RPC call to the TON API.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| method | str | yes | — | JSON-RPC method name |
| params | dict[str, Any] \| None | no | None | Method parameters |
| id | str | no | "1" | Request identifier |
| jsonrpc | str | no | "2.0" | JSON-RPC version string |

Returns: `Any` (raw JSON-RPC response)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 rpc json_rpc --method getMasterchainInfo
```

```python
result = await client.v2.rpc.json_rpc(
    "getAddressInformation",
    params={"address": "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"},
)
```
