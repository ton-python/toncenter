from __future__ import annotations

import typing as t

from toncenter.client import _get_adapter
from toncenter.rest.v2.models import (
    AddressInformation,
    ExtendedAddressInformation,
    TokenData,
    WalletInformation,
)
from toncenter.rest.v2.resources._base import BaseResource


class AccountsResource(BaseResource):
    """Access account and wallet information."""

    async def get_address_information(
        self,
        address: str,
        *,
        seqno: int | None = None,
    ) -> AddressInformation:
        """Get raw account state: balance, code, data, last transaction.

        :param address: Account address in any form.
        :param seqno: Optional masterchain block seqno for historical state.
        :return: ``AddressInformation``.
        """
        params: dict[str, t.Any] = {"address": address}
        if seqno is not None:
            params["seqno"] = seqno
        return await self._request(
            "GET",
            "/getAddressInformation",
            params=params,
            response_model=AddressInformation,
        )

    async def get_extended_address_information(
        self,
        address: str,
        *,
        seqno: int | None = None,
    ) -> ExtendedAddressInformation:
        """Get full account state including parsed account-state object.

        :param address: Account address in any form.
        :param seqno: Optional masterchain block seqno for historical state.
        :return: ``ExtendedAddressInformation``.
        """
        params: dict[str, t.Any] = {"address": address}
        if seqno is not None:
            params["seqno"] = seqno
        return await self._request(
            "GET",
            "/getExtendedAddressInformation",
            params=params,
            response_model=ExtendedAddressInformation,
        )

    async def get_wallet_information(
        self,
        address: str,
        *,
        seqno: int | None = None,
    ) -> WalletInformation:
        """Get wallet-specific information: type, seqno, balance.

        :param address: Account address in any form.
        :param seqno: Optional masterchain block seqno for historical state.
        :return: ``WalletInformation``.
        """
        params: dict[str, t.Any] = {"address": address}
        if seqno is not None:
            params["seqno"] = seqno
        return await self._request(
            "GET",
            "/getWalletInformation",
            params=params,
            response_model=WalletInformation,
        )

    async def get_address_balance(
        self,
        address: str,
        *,
        seqno: int | None = None,
    ) -> str:
        """Get account balance in nanotons.

        :param address: Account address in any form.
        :param seqno: Optional masterchain block seqno for historical state.
        :return: Balance as string.
        """
        params: dict[str, t.Any] = {"address": address}
        if seqno is not None:
            params["seqno"] = seqno
        return await self._request(
            "GET",
            "/getAddressBalance",
            params=params,
            response_model=str,
        )

    async def get_address_state(
        self,
        address: str,
        *,
        seqno: int | None = None,
    ) -> str:
        """Get account state: ``uninitialized``, ``active``, or ``frozen``.

        :param address: Account address in any form.
        :param seqno: Optional masterchain block seqno for historical state.
        :return: State string.
        """
        params: dict[str, t.Any] = {"address": address}
        if seqno is not None:
            params["seqno"] = seqno
        return await self._request(
            "GET",
            "/getAddressState",
            params=params,
            response_model=str,
        )

    async def get_token_data(
        self,
        address: str,
    ) -> TokenData:
        """Get Jetton or NFT metadata for a token contract.

        :param address: Token contract address in any form.
        :return: Token data (``JettonMasterData``, ``JettonWalletData``,
                 ``NftCollectionData``, or ``NftItemData``).
        """
        result = await self._request(
            "GET",
            "/getTokenData",
            params={"address": address},
        )
        return _get_adapter(TokenData).validate_python(result)  # type: ignore[no-any-return]
