# V3 Utils

2 methods from `client.v3.utils`:

## get_decode

Decode opcodes and message bodies via GET.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| opcodes | list[str] \| None | no | None | Opcodes to decode (hex with/without 0x prefix, or decimal) |
| bodies | list[str] \| None | no | None | Message bodies to decode (base64 or hex) |

Returns: `DecodeResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 utils get_decode --opcodes 0x0f8a7ea5
```

```python
result = await client.v3.utils.get_decode(opcodes=["0x0f8a7ea5", "0x7362d09c"])
```

## post_decode

Decode opcodes and message bodies via POST. Use for long parameters that may be truncated in GET.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | `DecodeRequest` | yes | — | Request body with `bodies: list[str] \| None` and `opcodes: list[str] \| None` |

Returns: `DecodeResponse`

```python
from toncenter.rest.v3.models import DecodeRequest

result = await client.v3.utils.post_decode(
    body=DecodeRequest(opcodes=["0x0f8a7ea5"], bodies=["te6cck..."]),
)
```

Note: `post_decode` is not easily callable via the runner due to the body object parameter. Use SDK code or `get_decode` for simple cases.
