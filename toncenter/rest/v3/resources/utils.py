from __future__ import annotations

from toncenter.rest.v3.models import DecodeRequest, DecodeResponse
from toncenter.rest.v3.resources._base import BaseResource


class UtilsResource(BaseResource):
    """Decode opcodes and message bodies."""

    async def get_decode(
        self,
        opcodes: list[str] | None = None,
        bodies: list[str] | None = None,
    ) -> DecodeResponse:
        """Decode opcodes and message bodies.

        Opcodes can be in hex (with or without 0x prefix) or decimal format. Bodies should be in base64 or hex format.

        :param opcodes: List of opcodes to decode (hex or decimal).
        :param bodies: List of message bodies to decode (base64 or hex).
        :return: ``DecodeResponse``.
        """
        path = "/decode"
        params = {
            "opcodes": opcodes,
            "bodies": bodies,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=DecodeResponse,
        )

    async def post_decode(
        self,
        body: DecodeRequest,
    ) -> DecodeResponse:
        """Decode opcodes and message bodies.

        Opcodes can be in hex (with or without 0x prefix) or decimal format. Bodies should be in base64 or hex format.
        Use POST method for long parameters that may be truncated in GET requests.

        :param body: Request body.
        :return: ``DecodeResponse``.
        """
        path = "/decode"
        return await self._request(
            method="POST",
            path=path,
            body=body.model_dump(),
            response_model=DecodeResponse,
        )
