# V2 Utils

4 methods from `client.v2.utils`:

## detect_address

Detect and parse an address, returning all format variants.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Address in any form |

Returns: ``DetectAddress``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 utils detect_address --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v2.utils.detect_address("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
```

## detect_hash

Detect and parse a hash, returning base64, base64url, and hex forms.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| hash | str | yes | — | Hash in any form |

Returns: ``DetectHash``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 utils detect_hash --hash abc123...
```

```python
result = await client.v2.utils.detect_hash("abc123...")
```

## pack_address

Convert a raw address to user-friendly format.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Raw address string |

Returns: `str`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 utils pack_address --address 0:ed1691307050047117b998b561d8de82d31fbf84910ced6eb5fc92e7485ef8a7
```

```python
packed = await client.v2.utils.pack_address("0:ed1691307050047117b998b561d8de82d31fbf84910ced6eb5fc92e7485ef8a7")
```

## unpack_address

Convert a user-friendly address to raw format.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | User-friendly base64 address |

Returns: `str`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 utils unpack_address --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
raw = await client.v2.utils.unpack_address("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
```
