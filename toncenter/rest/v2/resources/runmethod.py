from __future__ import annotations

import typing as t

from toncenter.rest.v2.models import (
    RunGetMethodResult,
    RunGetMethodStdResult,
)
from toncenter.rest.v2.resources._base import BaseResource


class RunmethodResource(BaseResource):
    """Execute get-methods on smart contracts."""

    async def run_get_method(
        self,
        address: str,
        method: str | int,
        stack: list[t.Any] | None = None,
        *,
        seqno: int | None = None,
    ) -> RunGetMethodResult:
        """Run a get-method on a smart contract (legacy stack format).

        :param address: Smart contract address in any form.
        :param method: Method name or numeric ID.
        :param stack: Input stack entries (legacy 2-tuple format).
        :param seqno: Optional masterchain block seqno.
        :return: ``RunGetMethodResult``.
        """
        body: dict[str, t.Any] = {
            "address": address,
            "method": method,
            "stack": stack or [],
        }
        if seqno is not None:
            body["seqno"] = seqno
        return await self._request(
            "POST",
            "/runGetMethod",
            body=body,
            response_model=RunGetMethodResult,
        )

    async def run_get_method_std(
        self,
        address: str,
        method: str | int,
        stack: list[t.Any] | None = None,
        *,
        seqno: int | None = None,
    ) -> RunGetMethodStdResult:
        """Run a get-method on a smart contract (typed TVM stack format).

        :param address: Smart contract address in any form.
        :param method: Method name or numeric ID.
        :param stack: Input TVM stack entries.
        :param seqno: Optional masterchain block seqno.
        :return: ``RunGetMethodStdResult``.
        """
        body: dict[str, t.Any] = {
            "address": address,
            "method": method,
            "stack": stack or [],
        }
        if seqno is not None:
            body["seqno"] = seqno
        return await self._request(
            "POST",
            "/runGetMethodStd",
            body=body,
            response_model=RunGetMethodStdResult,
        )
