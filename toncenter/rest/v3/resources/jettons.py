from __future__ import annotations

from toncenter.rest.v3.models import (
    JettonBurnsResponse,
    JettonMastersResponse,
    JettonTransfersResponse,
    JettonWalletsResponse,
)
from toncenter.rest.v3.resources._base import BaseResource


class JettonsResource(BaseResource):
    """Access Jetton masters, wallets, transfers and burns."""

    async def get_jetton_burns(
        self,
        address: list[str] | None = None,
        jetton_wallet: list[str] | None = None,
        jetton_master: str | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> JettonBurnsResponse:
        """Get Jetton burns by specified filters.

        :param address: Address of jetton wallet owner in any form. Max 1000.
        :param jetton_wallet: Jetton wallet address in any form. Max: 1000.
        :param jetton_master: Jetton master address in any form.
        :param start_utime: Query transactions with generation UTC timestamp **after** given timestamp.
        :param end_utime: Query transactions with generation UTC timestamp **before** given timestamp.
        :param start_lt: Query transactions with `lt >= start_lt`.
        :param end_lt: Query transactions with `lt <= end_lt`.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort transactions by lt.
        :return: ``JettonBurnsResponse``.
        """
        path = "/jetton/burns"
        params = {
            "address": address,
            "jetton_wallet": jetton_wallet,
            "jetton_master": jetton_master,
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
            response_model=JettonBurnsResponse,
        )

    async def get_jetton_masters(
        self,
        address: list[str] | None = None,
        admin_address: list[str] | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> JettonMastersResponse:
        """Get Jetton masters by specified filters.

        :param address: Jetton Master address in any form. Max: 1024.
        :param admin_address: Address of Jetton Master's admin in any form. Max: 1024.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: ``JettonMastersResponse``.
        """
        path = "/jetton/masters"
        params = {
            "address": address,
            "admin_address": admin_address,
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=JettonMastersResponse,
        )

    async def get_jetton_transfers(
        self,
        owner_address: list[str] | None = None,
        jetton_wallet: list[str] | None = None,
        jetton_master: str | None = None,
        direction: str | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> JettonTransfersResponse:
        """Get Jetton transfers by specified filters.

        :param owner_address: Address of jetton wallet owner in any form. Max 1000.
        :param jetton_wallet: Jetton wallet address in any form. Max: 1000.
        :param jetton_master: Jetton master address in any form.
        :param direction: Direction of transfer. *Note:* applied only with owner_address.
        :param start_utime: Query transactions with generation UTC timestamp **after** given timestamp.
        :param end_utime: Query transactions with generation UTC timestamp **before** given timestamp.
        :param start_lt: Query transactions with `lt >= start_lt`.
        :param end_lt: Query transactions with `lt <= end_lt`.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort transactions by lt.
        :return: ``JettonTransfersResponse``.
        """
        path = "/jetton/transfers"
        params = {
            "owner_address": owner_address,
            "jetton_wallet": jetton_wallet,
            "jetton_master": jetton_master,
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
            response_model=JettonTransfersResponse,
        )

    async def get_jetton_wallets(
        self,
        address: list[str] | None = None,
        owner_address: list[str] | None = None,
        jetton_address: list[str] | None = None,
        exclude_zero_balance: bool | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str | None = None,
    ) -> JettonWalletsResponse:
        """Get Jetton wallets by specified filters.

        :param address: Jetton wallet address in any form. Max: 1000.
        :param owner_address: Address of Jetton wallet's owner in any form. Max: 1000.
        :param jetton_address: Jetton Master in any form.
        :param exclude_zero_balance: Exclude jetton wallets with 0 balance.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort jetton wallets by balance. **Warning:** results may be inconsistent during the read with limit
            and offset.
        :return: ``JettonWalletsResponse``.
        """
        path = "/jetton/wallets"
        params = {
            "address": address,
            "owner_address": owner_address,
            "jetton_address": jetton_address,
            "exclude_zero_balance": exclude_zero_balance,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=JettonWalletsResponse,
        )
