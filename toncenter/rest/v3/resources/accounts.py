from __future__ import annotations

from toncenter.rest.v3.models import AccountStatesResponse, AddressBook, Metadata, WalletStatesResponse
from toncenter.rest.v3.resources._base import BaseResource


class AccountsResource(BaseResource):
    """Access account and wallet state information."""

    async def get_account_states(
        self,
        address: list[str],
        include_boc: bool = True,
    ) -> AccountStatesResponse:
        """Query account states.

        :param address: List of addresses in any form. Maximum 1000 addresses allowed.
        :param include_boc: Include code and data BOCs. Default: true.
        :return: ``AccountStatesResponse``.
        """
        path = "/accountStates"
        params = {
            "address": address,
            "include_boc": include_boc,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=AccountStatesResponse,
        )

    async def get_address_book(
        self,
        address: list[str],
    ) -> AddressBook:
        """Query address book.

        :param address: List of addresses in any form to get address book. Max: 1024.
        :return: ``AddressBook``.
        """
        path = "/addressBook"
        params = {"address": address}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=AddressBook,
        )

    async def get_metadata(
        self,
        address: list[str],
    ) -> Metadata:
        """Query address metadata.

        :param address: List of addresses in any form to get address metadata. Max: 1024.
        :return: ``Metadata``.
        """
        path = "/metadata"
        params = {"address": address}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=Metadata,
        )

    async def get_wallet_states(
        self,
        address: list[str],
    ) -> WalletStatesResponse:
        """Query wallet information.

        :param address: List of addresses in any form. Maximum 1000 addresses allowed.
        :return: ``WalletStatesResponse``.
        """
        path = "/walletStates"
        params = {"address": address}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=WalletStatesResponse,
        )
