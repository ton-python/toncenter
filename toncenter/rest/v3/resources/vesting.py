from __future__ import annotations

from toncenter.rest.v3.models import VestingContractsResponse
from toncenter.rest.v3.resources._base import BaseResource


class VestingResource(BaseResource):
    """Access vesting contracts."""

    async def get_vesting_contracts(
        self,
        contract_address: list[str] | None = None,
        wallet_address: list[str] | None = None,
        check_whitelist: bool = False,
        limit: int = 10,
        offset: int = 0,
    ) -> VestingContractsResponse:
        """Get vesting contracts by specified filters.

        :param contract_address: Vesting contract address in any form. Max: 1000.
        :param wallet_address: Wallet address to filter by owner or sender. Max: 1000.
        :param check_whitelist: Check if wallet address is in whitelist.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: ``VestingContractsResponse``.
        """
        path = "/vesting"
        params = {
            "contract_address": contract_address,
            "wallet_address": wallet_address,
            "check_whitelist": check_whitelist,
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=VestingContractsResponse,
        )
