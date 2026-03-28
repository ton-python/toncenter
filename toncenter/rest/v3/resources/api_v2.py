from __future__ import annotations

from toncenter.rest.v3.models import (
    V2AddressInformation,
    V2EstimateFeeRequest,
    V2EstimateFeeResult,
    V2RunGetMethodRequest,
    V2RunGetMethodResult,
    V2SendMessageRequest,
    V2SendMessageResult,
    V2WalletInformation,
)
from toncenter.rest.v3.resources._base import BaseResource


class ApiV2Resource(BaseResource):
    """Bridge to API v2 methods available through v3 endpoint."""

    async def get_address_information(
        self,
        address: str,
        use_v2: bool = True,
    ) -> V2AddressInformation:
        """Get smart contract information.

        :param address: Account address in any form.
        :param use_v2: Use method from api/v2. Not recommended.
        :return: ``V2AddressInformation``.
        """
        path = "/addressInformation"
        params = {
            "address": address,
            "use_v2": use_v2,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=V2AddressInformation,
        )

    async def estimate_fee(
        self,
        body: V2EstimateFeeRequest,
    ) -> V2EstimateFeeResult:
        """Estimate fees required for query processing.

        Fields body, init-code and init-data accepted in serialized format (b64-encoded).

        :param body: Request body.
        :return: ``V2EstimateFeeResult``.
        """
        path = "/estimateFee"
        return await self._request(
            method="POST",
            path=path,
            body=body.model_dump(),
            response_model=V2EstimateFeeResult,
        )

    async def send_message(
        self,
        body: V2SendMessageRequest,
    ) -> V2SendMessageResult:
        """Send an external message to the TON network.

        :param body: Request body.
        :return: ``V2SendMessageResult``.
        """
        path = "/message"
        return await self._request(
            method="POST",
            path=path,
            body=body.model_dump(),
            response_model=V2SendMessageResult,
        )

    async def run_get_method(
        self,
        body: V2RunGetMethodRequest,
    ) -> V2RunGetMethodResult:
        """Run a get-method on a smart contract.

        Stack supports ``num``, ``cell`` and ``slice`` types.

        :param body: Request body.
        :return: ``V2RunGetMethodResult``.
        """
        path = "/runGetMethod"
        return await self._request(
            method="POST",
            path=path,
            body=body.model_dump(),
            response_model=V2RunGetMethodResult,
        )

    async def get_wallet_information(
        self,
        address: str,
        use_v2: bool = True,
    ) -> V2WalletInformation:
        """Get wallet smart contract information.

        Supported wallets: ``v1r1``, ``v1r2``, ``v1r3``, ``v2r1``, ``v2r2``,
        ``v3r1``, ``v3r2``, ``v4r1``, ``v4r2``, ``v5beta``, ``v5r1``.
        Returns 409 if the account is not a wallet.

        :param address: Account address in any form.
        :param use_v2: Use method from api/v2. Not recommended.
        :return: ``V2WalletInformation``.
        """
        path = "/walletInformation"
        params = {
            "address": address,
            "use_v2": use_v2,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=V2WalletInformation,
        )
