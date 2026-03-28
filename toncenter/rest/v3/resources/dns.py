from __future__ import annotations

from toncenter.rest.v3.models import DNSRecordsResponse
from toncenter.rest.v3.resources._base import BaseResource


class DnsResource(BaseResource):
    """Access TON DNS records."""

    async def get_dns_records(
        self,
        wallet: str | None = None,
        domain: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> DNSRecordsResponse:
        """Query DNS records by specified filters. Currently .ton and .t.me DNS are supported.

        :param wallet: Wallet address in any form. DNS records that contain this address in wallet category will be
            returned.
        :param domain: Domain name to search for. DNS records with this exact domain name will be returned.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: ``DNSRecordsResponse``.
        """
        path = "/dns/records"
        params = {
            "wallet": wallet,
            "domain": domain,
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=DNSRecordsResponse,
        )
