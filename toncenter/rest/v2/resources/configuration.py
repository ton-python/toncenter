from __future__ import annotations

import typing as t

from toncenter.rest.v2.models import ConfigInfo, LibraryResult
from toncenter.rest.v2.resources._base import BaseResource


class ConfigurationResource(BaseResource):
    """Access blockchain configuration parameters and libraries."""

    async def get_config_param(
        self,
        param: int,
        *,
        seqno: int | None = None,
    ) -> ConfigInfo:
        """Get a single blockchain configuration parameter.

        :param param: Configuration parameter number.
        :param seqno: Optional masterchain block seqno for historical value.
        :return: ``ConfigInfo``.
        """
        params: dict[str, t.Any] = {"param": param}
        if seqno is not None:
            params["seqno"] = seqno
        return await self._request(
            "GET",
            "/getConfigParam",
            params=params,
            response_model=ConfigInfo,
        )

    async def get_config_all(self, *, seqno: int | None = None) -> ConfigInfo:
        """Get all blockchain configuration parameters.

        :param seqno: Optional masterchain block seqno for historical values.
        :return: ``ConfigInfo``.
        """
        params: dict[str, t.Any] = {}
        if seqno is not None:
            params["seqno"] = seqno
        return await self._request(
            "GET",
            "/getConfigAll",
            params=params,
            response_model=ConfigInfo,
        )

    async def get_libraries(self, libraries: list[str]) -> LibraryResult:
        """Get library code by hash list.

        :param libraries: List of library cell hashes.
        :return: ``LibraryResult``.
        """
        return await self._request(
            "GET",
            "/getLibraries",
            params={"libraries": libraries},
            response_model=LibraryResult,
        )
