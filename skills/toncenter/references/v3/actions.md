# V3 Actions

4 methods from `client.v3.actions`:

## get_actions

Get parsed actions with extensive filtering options.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account | str \| None | no | None | Account address (hex/base64/base64url) |
| tx_hash | list[str] \| None | no | None | Find actions by transaction hash |
| msg_hash | list[str] \| None | no | None | Find actions by message hash |
| action_id | list[str] \| None | no | None | Find actions by action_id |
| trace_id | list[str] \| None | no | None | Find actions by trace_id |
| mc_seqno | int \| None | no | None | Actions from traces completed in this masterchain block |
| start_utime | int \| None | no | None | Traces with trace_end_utime >= start_utime |
| end_utime | int \| None | no | None | Traces with trace_end_utime <= end_utime |
| start_lt | int \| None | no | None | Traces with trace_end_lt >= start_lt |
| end_lt | int \| None | no | None | Traces with trace_end_lt <= end_lt |
| action_type | list[str] \| None | no | None | Include these action types |
| exclude_action_type | list[str] \| None | no | None | Exclude these action types |
| supported_action_types | list[str] \| None | no | None | Supported action types |
| include_accounts | bool | no | False | Include accounts array for each action |
| include_transactions | bool | no | False | Include transactions_full array |
| limit | int | no | 10 | Max results (1-256) |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort by lt: "asc" or "desc" |

Returns: ``ActionsResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 actions get_actions --account EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v3.actions.get_actions(
    account="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    limit=5,
)
```

## get_pending_actions

Get pending (unfinalized) actions.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account | str \| None | no | None | Account address (hex/base64/base64url) |
| ext_msg_hash | list[str] \| None | no | None | Find actions by trace external hash |
| supported_action_types | list[str] \| None | no | None | Supported action types |
| include_transactions | bool | no | False | Include transactions_full array |

Returns: ``ActionsResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 actions get_pending_actions --account EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v3.actions.get_pending_actions(
    account="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
)
```

## get_pending_traces

Get pending (unfinalized) traces.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account | str \| None | no | None | Account address (hex/base64/base64url) |
| ext_msg_hash | list[str] \| None | no | None | Find trace by external hash |

Returns: ``TracesResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 actions get_pending_traces --account EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v3.actions.get_pending_traces(
    account="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
)
```

## get_traces

Get traces with filtering options.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account | str \| None | no | None | Account address (hex/base64/base64url) |
| trace_id | list[str] \| None | no | None | Find trace by trace id |
| tx_hash | list[str] \| None | no | None | Find trace by transaction hash |
| msg_hash | list[str] \| None | no | None | Find trace by message hash |
| mc_seqno | int \| None | no | None | Traces completed in this masterchain block |
| start_utime | int \| None | no | None | Traces finished after given timestamp |
| end_utime | int \| None | no | None | Traces finished before given timestamp |
| start_lt | int \| None | no | None | Traces with end_lt >= start_lt |
| end_lt | int \| None | no | None | Traces with end_lt <= end_lt |
| include_actions | bool | no | False | Include trace actions |
| supported_action_types | list[str] \| None | no | None | Supported action types |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort by lt: "asc" or "desc" |

Returns: ``TracesResponse``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 actions get_traces --account EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v3.actions.get_traces(
    account="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    limit=5,
    include_actions=True,
)
```
