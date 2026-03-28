from __future__ import annotations

import typing as t

from toncenter.rest.v2.models import (
    BlockTransactions,
    BlockTransactionsExt,
    Transaction,
    TransactionsStd,
)
from toncenter.rest.v2.resources._base import BaseResource


class TransactionsResource(BaseResource):
    """Access transaction data from the blockchain."""

    async def get_block_transactions(
        self,
        workchain: int,
        shard: str,
        seqno: int,
        *,
        root_hash: str | None = None,
        file_hash: str | None = None,
        after_lt: str | None = None,
        after_hash: str | None = None,
        count: int | None = None,
    ) -> BlockTransactions:
        """Get transaction IDs in a specific block.

        :param workchain: Workchain ID.
        :param shard: Shard ID.
        :param seqno: Block sequence number.
        :param root_hash: Optional root hash for verification.
        :param file_hash: Optional file hash for verification.
        :param after_lt: Return transactions after this logical time.
        :param after_hash: Account hash (hex or base64) to read transactions after.
        :param count: Maximum number of transactions to return.
        :return: ``BlockTransactions``.
        """
        params: dict[str, t.Any] = {
            "workchain": workchain,
            "shard": shard,
            "seqno": seqno,
        }
        if root_hash is not None:
            params["root_hash"] = root_hash
        if file_hash is not None:
            params["file_hash"] = file_hash
        if after_lt is not None:
            params["after_lt"] = after_lt
        if after_hash is not None:
            params["after_hash"] = after_hash
        if count is not None:
            params["count"] = count
        return await self._request(
            "GET",
            "/getBlockTransactions",
            params=params,
            response_model=BlockTransactions,
        )

    async def get_block_transactions_ext(
        self,
        workchain: int,
        shard: str,
        seqno: int,
        *,
        root_hash: str | None = None,
        file_hash: str | None = None,
        after_lt: str | None = None,
        after_hash: str | None = None,
        count: int | None = None,
    ) -> BlockTransactionsExt:
        """Get full transactions in a specific block.

        :param workchain: Workchain ID.
        :param shard: Shard ID.
        :param seqno: Block sequence number.
        :param root_hash: Optional root hash for verification.
        :param file_hash: Optional file hash for verification.
        :param after_lt: Return transactions after this logical time.
        :param after_hash: Account hash (hex or base64) to read transactions after.
        :param count: Maximum number of transactions to return.
        :return: ``BlockTransactionsExt``.
        """
        params: dict[str, t.Any] = {
            "workchain": workchain,
            "shard": shard,
            "seqno": seqno,
        }
        if root_hash is not None:
            params["root_hash"] = root_hash
        if file_hash is not None:
            params["file_hash"] = file_hash
        if after_lt is not None:
            params["after_lt"] = after_lt
        if after_hash is not None:
            params["after_hash"] = after_hash
        if count is not None:
            params["count"] = count
        return await self._request(
            "GET",
            "/getBlockTransactionsExt",
            params=params,
            response_model=BlockTransactionsExt,
        )

    async def get_transactions(
        self,
        address: str,
        *,
        limit: int = 10,
        lt: str | None = None,
        hash: str | None = None,
        to_lt: str | None = None,
        archival: bool | None = None,
    ) -> list[Transaction]:
        """Get transactions for an address.

        :param address: Account address in any form.
        :param limit: Maximum number of transactions (default 10).
        :param lt: Start from this logical time (pagination).
        :param hash: Start from this transaction hash (pagination).
        :param to_lt: Return transactions up to this logical time.
        :param archival: Use archival node for old transactions.
        :return: List of ``Transaction``.
        """
        params: dict[str, t.Any] = {"address": address, "limit": limit}
        if lt is not None:
            params["lt"] = lt
        if hash is not None:
            params["hash"] = hash
        if to_lt is not None:
            params["to_lt"] = to_lt
        if archival is not None:
            params["archival"] = archival
        return await self._request(
            "GET",
            "/getTransactions",
            params=params,
            response_model=list[Transaction],
        )

    async def get_transactions_std(
        self,
        address: str,
        *,
        limit: int = 10,
        lt: str | None = None,
        hash: str | None = None,
        to_lt: str | None = None,
        archival: bool | None = None,
    ) -> TransactionsStd:
        """Get transactions in standardized raw format.

        :param address: Account address in any form.
        :param limit: Maximum number of transactions (default 10).
        :param lt: Start from this logical time (pagination).
        :param hash: Start from this transaction hash (pagination).
        :param to_lt: Return transactions up to this logical time.
        :param archival: Use archival node for old transactions.
        :return: ``TransactionsStd``.
        """
        params: dict[str, t.Any] = {"address": address, "limit": limit}
        if lt is not None:
            params["lt"] = lt
        if hash is not None:
            params["hash"] = hash
        if to_lt is not None:
            params["to_lt"] = to_lt
        if archival is not None:
            params["archival"] = archival
        return await self._request(
            "GET",
            "/getTransactionsStd",
            params=params,
            response_model=TransactionsStd,
        )

    async def try_locate_tx(
        self,
        source: str,
        destination: str,
        created_lt: str,
    ) -> Transaction:
        """Locate outgoing transaction of destination address by incoming message.

        :param source: Source address in any form.
        :param destination: Destination address in any form.
        :param created_lt: Creation logical time of the message.
        :return: ``Transaction``.
        """
        return await self._request(
            "GET",
            "/tryLocateTx",
            params={
                "source": source,
                "destination": destination,
                "created_lt": created_lt,
            },
            response_model=Transaction,
        )

    async def try_locate_result_tx(
        self,
        source: str,
        destination: str,
        created_lt: str,
    ) -> Transaction:
        """Locate result transaction of an outbound message.

        :param source: Source address in any form.
        :param destination: Destination address in any form.
        :param created_lt: Creation logical time of the message.
        :return: ``Transaction``.
        """
        return await self._request(
            "GET",
            "/tryLocateResultTx",
            params={
                "source": source,
                "destination": destination,
                "created_lt": created_lt,
            },
            response_model=Transaction,
        )

    async def try_locate_source_tx(
        self,
        source: str,
        destination: str,
        created_lt: str,
    ) -> Transaction:
        """Locate source transaction by destination transaction parameters.

        :param source: Source address in any form.
        :param destination: Destination address in any form.
        :param created_lt: Creation logical time of the message.
        :return: ``Transaction``.
        """
        return await self._request(
            "GET",
            "/tryLocateSourceTx",
            params={
                "source": source,
                "destination": destination,
                "created_lt": created_lt,
            },
            response_model=Transaction,
        )
