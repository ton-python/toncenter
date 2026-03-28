from __future__ import annotations

from toncenter.rest.v2.models import ExtMessageInfo, QueryFees, ResultOk
from toncenter.rest.v2.resources._base import BaseResource


class SendResource(BaseResource):
    """Send messages to the blockchain and estimate fees."""

    async def send_boc(self, boc: str) -> ResultOk:
        """Send a serialized bag-of-cells to the network.

        :param boc: Base64-encoded serialized BoC.
        :return: ``ResultOk``.
        """
        return await self._request(
            "POST",
            "/sendBoc",
            body={"boc": boc},
            response_model=ResultOk,
        )

    async def send_boc_return_hash(self, boc: str) -> ExtMessageInfo:
        """Send a BoC and return the message hash.

        :param boc: Base64-encoded serialized BoC.
        :return: ``ExtMessageInfo``.
        """
        return await self._request(
            "POST",
            "/sendBocReturnHash",
            body={"boc": boc},
            response_model=ExtMessageInfo,
        )

    async def estimate_fee(
        self,
        address: str,
        body: str,
        *,
        init_code: str = "",
        init_data: str = "",
        ignore_chksig: bool = True,
    ) -> QueryFees:
        """Estimate fees for sending a message.

        :param address: Destination address in any form.
        :param body: Base64-encoded message body BoC.
        :param init_code: Base64-encoded init code (for deploy).
        :param init_data: Base64-encoded init data (for deploy).
        :param ignore_chksig: Skip signature check (default ``True``).
        :return: ``QueryFees``.
        """
        return await self._request(
            "POST",
            "/estimateFee",
            body={
                "address": address,
                "body": body,
                "init_code": init_code,
                "init_data": init_data,
                "ignore_chksig": ignore_chksig,
            },
            response_model=QueryFees,
        )
