from __future__ import annotations

import typing as t

from toncenter.rest.v2.resources._base import BaseResource


class RpcResource(BaseResource):
    """JSON-RPC interface for the TON API."""

    async def json_rpc(
        self,
        method: str,
        *,
        params: dict[str, t.Any] | None = None,
        id: str = "1",
        jsonrpc: str = "2.0",
    ) -> t.Any:
        """Execute a JSON-RPC request.

        :param method: JSON-RPC method name.
        :param params: Method parameters.
        :param id: Request identifier.
        :param jsonrpc: JSON-RPC version string.
        :return: Raw JSON-RPC response.
        """
        body: dict[str, t.Any] = {
            "method": method,
            "params": params or {},
            "id": id,
            "jsonrpc": jsonrpc,
        }
        return await self._request(
            "POST",
            "/jsonRPC",
            body=body,
        )
