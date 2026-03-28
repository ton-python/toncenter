# V3 Stats

1 method from `client.v3.stats`:

## get_top_accounts_by_balance

Get top accounts ranked by balance.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: ``list[AccountBalance]``

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 stats get_top_accounts_by_balance --limit 10
```

```python
result = await client.v3.stats.get_top_accounts_by_balance(limit=10)
```
