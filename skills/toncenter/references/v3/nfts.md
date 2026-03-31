# V3 NFTs

4 methods from `client.v3.nfts`:

## get_nft_collections

Get NFT collections.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| collection_address | list[str] \| None | no | None | Collection address in any form (max 1024) |
| owner_address | list[str] \| None | no | None | Collection owner address in any form (max 1024) |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: `NFTCollectionsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 nfts get_nft_collections --limit 5
```

```python
result = await client.v3.nfts.get_nft_collections(limit=5)
```

## get_nft_items

Get NFT items with filtering.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] \| None | no | None | NFT item address in any form (max 1000) |
| owner_address | list[str] \| None | no | None | NFT owner address in any form (max 1000) |
| collection_address | list[str] \| None | no | None | Collection address in any form |
| index | list[str] \| None | no | None | Item index for given collection (max 1000) |
| include_on_sale | bool | no | False | Include NFTs on sales/auctions (only with owner_address) |
| sort_by_last_transaction_lt | bool \| None | no | None | Sort by last transaction lt desc (may be inconsistent during pagination) |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: `NFTItemsResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 nfts get_nft_items --owner-address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v3.nfts.get_nft_items(
    owner_address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    limit=5,
)
```

## get_nft_sales

Get NFT sale/auction contracts.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | list[str] | yes | — | Sale or auction contract address in any form (max 1000) |

Returns: `NFTSalesResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 nfts get_nft_sales --address EQ...
```

```python
result = await client.v3.nfts.get_nft_sales(address=["EQ..."])
```

## get_nft_transfers

Get NFT transfer history.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| owner_address | list[str] \| None | no | None | NFT owner address in any form (max 1000) |
| item_address | list[str] \| None | no | None | NFT item address in any form (max 1000) |
| collection_address | str \| None | no | None | Collection address in any form |
| direction | str \| None | no | None | Direction of transfer |
| start_utime | int \| None | no | None | Transfers after given timestamp |
| end_utime | int \| None | no | None | Transfers before given timestamp |
| start_lt | int \| None | no | None | Transfers with lt >= start_lt |
| end_lt | int \| None | no | None | Transfers with lt <= end_lt |
| limit | int | no | 10 | Max results |
| offset | int | no | 0 | Pagination offset |
| sort | str | no | "desc" | Sort: "asc" or "desc" |

Returns: `NFTTransfersResponse`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 nfts get_nft_transfers --owner-address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 --limit 5
```

```python
result = await client.v3.nfts.get_nft_transfers(
    owner_address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    limit=5,
)
```
