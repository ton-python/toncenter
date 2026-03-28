from __future__ import annotations

from toncenter.rest.v3.models import MultisigOrderResponse, MultisigResponse
from toncenter.rest.v3.resources._base import BaseResource


class MultisigResource(BaseResource):
    """Access multisig wallets and orders."""

    async def get_multisig_orders(
        self,
        address: list[str] | None = None,
        multisig_address: list[str] | None = None,
        parse_actions: bool = False,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> MultisigOrderResponse:
        """Get multisig orders by specified filters.

        :param address: Order address in any form. Max: 1024.
        :param multisig_address: Address of corresponding multisig. Max: 1024.
        :param parse_actions: Parse order actions.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort orders by last_transaction_lt.
        :return: ``MultisigOrderResponse``.
        """
        path = "/multisig/orders"
        params = {
            "address": address,
            "multisig_address": multisig_address,
            "parse_actions": parse_actions,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=MultisigOrderResponse,
        )

    async def get_multisig_wallets(
        self,
        address: list[str] | None = None,
        wallet_address: list[str] | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
        include_orders: bool = True,
    ) -> MultisigResponse:
        """Get multisig contracts by specified filters with associated orders.

        :param address: Multisig contract address in any form. Max: 1024.
        :param wallet_address: Address of signer or proposer wallet in any form. Max: 1024.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort multisigs by last_transaction_lt.
        :param include_orders: Gather multisig orders.
        :return: ``MultisigResponse``.
        """
        path = "/multisig/wallets"
        params = {
            "address": address,
            "wallet_address": wallet_address,
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "include_orders": include_orders,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=MultisigResponse,
        )
