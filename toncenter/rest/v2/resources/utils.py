from __future__ import annotations

from toncenter.rest.v2.models import DetectAddress, DetectHash
from toncenter.rest.v2.resources._base import BaseResource


class UtilsResource(BaseResource):
    """Address detection and packing utilities."""

    async def detect_address(self, address: str) -> DetectAddress:
        """Get all known forms of a TON address.

        :param address: Address in any form.
        :return: ``DetectAddress``.
        """
        return await self._request(
            "GET",
            "/detectAddress",
            params={"address": address},
            response_model=DetectAddress,
        )

    async def detect_hash(self, hash: str) -> DetectHash:
        """Get all known forms of a 256-bit hash.

        :param hash: Hash in any form.
        :return: ``DetectHash``.
        """
        return await self._request(
            "GET",
            "/detectHash",
            params={"hash": hash},
            response_model=DetectHash,
        )

    async def pack_address(self, address: str) -> str:
        """Pack a raw address into user-friendly base64 form.

        :param address: Raw address string.
        :return: Packed address string.
        """
        return await self._request(
            "GET",
            "/packAddress",
            params={"address": address},
            response_model=str,
        )

    async def unpack_address(self, address: str) -> str:
        """Unpack a user-friendly address into raw form.

        :param address: User-friendly base64 address.
        :return: Raw address string.
        """
        return await self._request(
            "GET",
            "/unpackAddress",
            params={"address": address},
            response_model=str,
        )
