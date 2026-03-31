# V2 Configuration

3 methods from `client.v2.configuration`:

## get_config_param

Get a specific blockchain configuration parameter.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| param | int | yes | — | Configuration parameter number |
| seqno | int \| None | no | None | Masterchain block seqno for historical value |

Returns: `ConfigInfo`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 configuration get_config_param --param 34
```

```python
config = await client.v2.configuration.get_config_param(34)
```

## get_config_all

Get all blockchain configuration parameters.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| seqno | int \| None | no | None | Masterchain block seqno for historical values |

Returns: `ConfigInfo`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 configuration get_config_all
```

```python
config = await client.v2.configuration.get_config_all()
```

## get_libraries

Get library cells by their hashes.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| libraries | list[str] | yes | — | List of library cell hashes |

Returns: `LibraryResult`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v2 configuration get_libraries --libraries a1b2c3...
```

```python
libs = await client.v2.configuration.get_libraries(["a1b2c3...", "d4e5f6..."])
```
