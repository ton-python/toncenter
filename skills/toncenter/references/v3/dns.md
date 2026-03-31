# V3 DNS

1 method from `client.v3.dns`:

## get_dns_records

Get TON DNS records.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| wallet | str \| None | no | None | Wallet address in any form (returns records containing this address) |
| domain | str \| None | no | None | Domain name to search for (exact match) |
| limit | int | no | 100 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: `DNSRecordsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 dns get_dns_records --domain ton.org
```

```python
result = await client.v3.dns.get_dns_records(domain="ton.org")
```
