from __future__ import annotations

from toncenter.rest.v3.models import NFTCollectionsResponse, NFTItemsResponse, NFTSalesResponse, NFTTransfersResponse
from toncenter.rest.v3.resources._base import BaseResource


class NftsResource(BaseResource):
    """Access NFT collections, items, transfers and sales."""

    async def get_nft_collections(
        self,
        collection_address: list[str] | None = None,
        owner_address: list[str] | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> NFTCollectionsResponse:
        """Get NFT collections by specified filters.

        :param collection_address: Collection address in any form. Max: 1024.
        :param owner_address: Address of collection owner in any form. Max: 1024.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: ``NFTCollectionsResponse``.
        """
        path = "/nft/collections"
        params = {
            "collection_address": collection_address,
            "owner_address": owner_address,
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=NFTCollectionsResponse,
        )

    async def get_nft_items(
        self,
        address: list[str] | None = None,
        owner_address: list[str] | None = None,
        collection_address: list[str] | None = None,
        index: list[str] | None = None,
        include_on_sale: bool = False,
        sort_by_last_transaction_lt: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> NFTItemsResponse:
        """Get NFT items by specified filters.

        :param address: NFT item address in any form. Max: 1000.
        :param owner_address: Address of NFT item owner in any form. Max: 1000.
        :param collection_address: Collection address in any form.
        :param index: Index of item for given collection. Max: 1000.
        :param include_on_sale: Include nft on sales and auctions. Used only when owner_address is passed.
        :param sort_by_last_transaction_lt: Sort NFT items by last transaction lt descending. **Warning:** results may
            be inconsistent during pagination with limit and offset.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: ``NFTItemsResponse``.
        """
        path = "/nft/items"
        params = {
            "address": address,
            "owner_address": owner_address,
            "collection_address": collection_address,
            "index": index,
            "include_on_sale": include_on_sale,
            "sort_by_last_transaction_lt": sort_by_last_transaction_lt,
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=NFTItemsResponse,
        )

    async def get_nft_sales(
        self,
        address: list[str],
    ) -> NFTSalesResponse:
        """Get GetGems NFT sales and auctions by sale/auction contract addresses.

        :param address: Sale or auction contract address in any form. Max: 1000.
        :return: ``NFTSalesResponse``.
        """
        path = "/nft/sales"
        params = {"address": address}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=NFTSalesResponse,
        )

    async def get_nft_transfers(
        self,
        owner_address: list[str] | None = None,
        item_address: list[str] | None = None,
        collection_address: str | None = None,
        direction: str | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> NFTTransfersResponse:
        """Get transfers of NFT items by specified filters.

        :param owner_address: Address of NFT owner in any form. Max 1000.
        :param item_address: Address of NFT item in any form. Max: 1000.
        :param collection_address: Collection address in any form.
        :param direction: Direction of transfer.
        :param start_utime: Query transactions with generation UTC timestamp **after** given timestamp.
        :param end_utime: Query transactions with generation UTC timestamp **before** given timestamp.
        :param start_lt: Query transactions with `lt >= start_lt`.
        :param end_lt: Query transactions with `lt <= end_lt`.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort transactions by lt.
        :return: ``NFTTransfersResponse``.
        """
        path = "/nft/transfers"
        params = {
            "owner_address": owner_address,
            "item_address": item_address,
            "collection_address": collection_address,
            "direction": direction,
            "start_utime": start_utime,
            "end_utime": end_utime,
            "start_lt": start_lt,
            "end_lt": end_lt,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=NFTTransfersResponse,
        )
