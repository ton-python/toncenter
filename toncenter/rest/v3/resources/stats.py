from __future__ import annotations

from toncenter.rest.v3.models import AccountBalance
from toncenter.rest.v3.resources._base import BaseResource


class StatsResource(BaseResource):
    """Access blockchain statistics."""

    async def get_top_accounts_by_balance(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> list[AccountBalance]:
        """Get list of accounts sorted descending by balance.

        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: List of ``AccountBalance``.
        """
        path = "/topAccountsByBalance"
        params = {
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=list[AccountBalance],
        )
