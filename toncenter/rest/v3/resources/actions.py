from __future__ import annotations

from toncenter.rest.v3.models import ActionsResponse, TracesResponse
from toncenter.rest.v3.resources._base import BaseResource


class ActionsResource(BaseResource):
    """Access parsed action and trace data."""

    async def get_actions(
        self,
        account: str | None = None,
        tx_hash: list[str] | None = None,
        msg_hash: list[str] | None = None,
        action_id: list[str] | None = None,
        trace_id: list[str] | None = None,
        mc_seqno: int | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        action_type: list[str] | None = None,
        exclude_action_type: list[str] | None = None,
        supported_action_types: list[str] | None = None,
        include_accounts: bool = False,
        include_transactions: bool = False,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> ActionsResponse:
        """Get actions by specified filter.

        :param account: Account address in hex, base64 or base64url form.
        :param tx_hash: Find actions by transaction hash.
        :param msg_hash: Find actions by message hash.
        :param action_id: Find actions by the action_id.
        :param trace_id: Find actions by the trace_id.
        :param mc_seqno: Query actions of traces which was completed in masterchain block with given seqno.
        :param start_utime: Query actions for traces with `trace_end_utime >= start_utime`.
        :param end_utime: Query actions for traces with `trace_end_utime <= end_utime`.
        :param start_lt: Query actions for traces with `trace_end_lt >= start_lt`.
        :param end_lt: Query actions for traces with `trace_end_lt <= end_lt`.
        :param action_type: Include action types.
        :param exclude_action_type: Exclude action types.
        :param supported_action_types: Supported action types.
        :param include_accounts: Include accounts array for each action in response.
        :param include_transactions: Include `transactions_full` array with detailed transaction data for each action in
            response.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort actions by lt.
        :return: ``ActionsResponse``.
        """
        path = "/actions"
        params = {
            "account": account,
            "tx_hash": tx_hash,
            "msg_hash": msg_hash,
            "action_id": action_id,
            "trace_id": trace_id,
            "mc_seqno": mc_seqno,
            "start_utime": start_utime,
            "end_utime": end_utime,
            "start_lt": start_lt,
            "end_lt": end_lt,
            "action_type": action_type,
            "exclude_action_type": exclude_action_type,
            "supported_action_types": supported_action_types,
            "include_accounts": include_accounts,
            "include_transactions": include_transactions,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=ActionsResponse,
        )

    async def get_pending_actions(
        self,
        account: str | None = None,
        ext_msg_hash: list[str] | None = None,
        supported_action_types: list[str] | None = None,
        include_transactions: bool = False,
    ) -> ActionsResponse:
        """Get pending actions by specified filter.

        :param account: Account address in hex, base64 or base64url form.
        :param ext_msg_hash: Find actions by trace external hash.
        :param supported_action_types: Supported action types.
        :param include_transactions: Include `transactions_full` array with detailed transaction data for each action in
            response.
        :return: ``ActionsResponse``.
        """
        path = "/pendingActions"
        params = {
            "account": account,
            "ext_msg_hash": ext_msg_hash,
            "supported_action_types": supported_action_types,
            "include_transactions": include_transactions,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=ActionsResponse,
        )

    async def get_pending_traces(
        self,
        account: str | None = None,
        ext_msg_hash: list[str] | None = None,
    ) -> TracesResponse:
        """Get pending traces by specified filter.

        :param account: Account address in hex, base64 or base64url form.
        :param ext_msg_hash: Find trace by external hash.
        :return: ``TracesResponse``.
        """
        path = "/pendingTraces"
        params = {
            "account": account,
            "ext_msg_hash": ext_msg_hash,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=TracesResponse,
        )

    async def get_traces(
        self,
        account: str | None = None,
        trace_id: list[str] | None = None,
        tx_hash: list[str] | None = None,
        msg_hash: list[str] | None = None,
        mc_seqno: int | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        include_actions: bool = False,
        supported_action_types: list[str] | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> TracesResponse:
        """Get traces by specified filter.

        :param account: Account address in hex, base64 or base64url form.
        :param trace_id: Find trace by trace id.
        :param tx_hash: Find trace by transaction hash.
        :param msg_hash: Find trace by message hash.
        :param mc_seqno: Query traces that was completed in masterchain block with given seqno.
        :param start_utime: Query traces, which was finished **after** given timestamp.
        :param end_utime: Query traces, which was finished **before** given timestamp.
        :param start_lt: Query traces with `end_lt >= start_lt`.
        :param end_lt: Query traces with `end_lt <= end_lt`.
        :param include_actions: Include trace actions.
        :param supported_action_types: Supported action types.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort traces by lt.
        :return: ``TracesResponse``.
        """
        path = "/traces"
        params = {
            "account": account,
            "trace_id": trace_id,
            "tx_hash": tx_hash,
            "msg_hash": msg_hash,
            "mc_seqno": mc_seqno,
            "start_utime": start_utime,
            "end_utime": end_utime,
            "start_lt": start_lt,
            "end_lt": end_lt,
            "include_actions": include_actions,
            "supported_action_types": supported_action_types,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=TracesResponse,
        )
