from __future__ import annotations

from toncenter.rest.v3.models import BlocksResponse, MasterchainInfo, MessagesResponse, TransactionsResponse
from toncenter.rest.v3.resources._base import BaseResource


class BlockchainResource(BaseResource):
    """Access blockchain state, blocks, transactions and messages."""

    async def get_adjacent_transactions(
        self,
        hash: str | None = None,
        direction: str | None = None,
    ) -> TransactionsResponse:
        """Get parent and/or children for specified transaction.

        :param hash: Transaction hash.
        :param direction: Direction of message.
        :return: ``TransactionsResponse``.
        """
        path = "/adjacentTransactions"
        params = {
            "hash": hash,
            "direction": direction,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=TransactionsResponse,
        )

    async def get_blocks(
        self,
        workchain: int | None = None,
        shard: str | None = None,
        seqno: int | None = None,
        root_hash: str | None = None,
        file_hash: str | None = None,
        mc_seqno: int | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> BlocksResponse:
        """Return blocks by specified filters.

        :param workchain: Block workchain.
        :param shard: Block shard id. Must be sent with *workchain*. Example: `8000000000000000`.
        :param seqno: Block seqno. Must be sent with *workchain* and *shard*.
        :param root_hash: Block root hash.
        :param file_hash: Block file hash.
        :param mc_seqno: Masterchain block seqno.
        :param start_utime: Query blocks with generation UTC timestamp **after** given timestamp.
        :param end_utime: Query blocks with generation UTC timestamp **before** given timestamp.
        :param start_lt: Query blocks with `lt >= start_lt`.
        :param end_lt: Query blocks with `lt <= end_lt`.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort results by UTC timestamp.
        :return: ``BlocksResponse``.
        """
        path = "/blocks"
        params = {
            "workchain": workchain,
            "shard": shard,
            "seqno": seqno,
            "root_hash": root_hash,
            "file_hash": file_hash,
            "mc_seqno": mc_seqno,
            "start_utime": start_utime,
            "end_utime": end_utime,
            "start_lt": start_lt,
            "end_lt": end_lt,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=BlocksResponse,
        )

    async def get_masterchain_block_shard_state(
        self,
        seqno: int,
    ) -> BlocksResponse:
        """Get masterchain block shard state. Same as /api/v2/shards.

        :param seqno: Masterchain block seqno.
        :return: ``BlocksResponse``.
        """
        path = "/masterchainBlockShardState"
        params = {"seqno": seqno}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=BlocksResponse,
        )

    async def get_masterchain_block_shards(
        self,
        seqno: int,
        limit: int = 10,
        offset: int = 0,
    ) -> BlocksResponse:
        """Return all workchain blocks that appeared after the previous masterchain block.

        :param seqno: Masterchain block seqno.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: ``BlocksResponse``.
        """
        path = "/masterchainBlockShards"
        params = {
            "seqno": seqno,
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=BlocksResponse,
        )

    async def get_masterchain_info(
        self,
    ) -> MasterchainInfo:
        """Get first and last indexed block.

        :return: ``MasterchainInfo``.
        """
        path = "/masterchainInfo"
        return await self._request(
            method="GET",
            path=path,
            response_model=MasterchainInfo,
        )

    async def get_messages(
        self,
        msg_hash: list[str] | None = None,
        body_hash: str | None = None,
        source: str | None = None,
        destination: str | None = None,
        opcode: str | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        direction: str | None = None,
        exclude_externals: bool | None = None,
        only_externals: bool | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> MessagesResponse:
        """Get messages by specified filters.

        :param msg_hash: Message hash. Acceptable in hex, base64 and base64url forms.
        :param body_hash: Hash of message body.
        :param source: The source account address. Can be sent in hex, base64 or base64url form. Use value `null` to get
            external messages.
        :param destination: The destination account address. Can be sent in hex, base64 or base64url form. Use value
            `null` to get log messages.
        :param opcode: Opcode of message in hex or signed 32-bit decimal form.
        :param start_utime: Query messages with `created_at >= start_utime`.
        :param end_utime: Query messages with `created_at <= end_utime`.
        :param start_lt: Query messages with `created_lt >= start_lt`.
        :param end_lt: Query messages with `created_lt <= end_lt`.
        :param direction: Direction of message.
        :param exclude_externals: Exclude external messages.
        :param only_externals: Return only external messages.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort messages by lt. When set to ``desc``, set ``start_lt=1`` to get latest messages.
        :return: ``MessagesResponse``.
        """
        path = "/messages"
        params = {
            "msg_hash": msg_hash,
            "body_hash": body_hash,
            "source": source,
            "destination": destination,
            "opcode": opcode,
            "start_utime": start_utime,
            "end_utime": end_utime,
            "start_lt": start_lt,
            "end_lt": end_lt,
            "direction": direction,
            "exclude_externals": exclude_externals,
            "only_externals": only_externals,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=MessagesResponse,
        )

    async def get_pending_transactions(
        self,
        account: list[str] | None = None,
        trace_id: list[str] | None = None,
    ) -> TransactionsResponse:
        """Get pending transactions by specified filter.

        :param account: List of account addresses to get transactions. Can be sent in hex, base64 or base64url form.
        :param trace_id: Find transactions by trace id.
        :return: ``TransactionsResponse``.
        """
        path = "/pendingTransactions"
        params = {
            "account": account,
            "trace_id": trace_id,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=TransactionsResponse,
        )

    async def get_transactions(
        self,
        workchain: int | None = None,
        shard: str | None = None,
        seqno: int | None = None,
        mc_seqno: int | None = None,
        account: list[str] | None = None,
        exclude_account: list[str] | None = None,
        hash: str | None = None,
        lt: int | None = None,
        start_utime: int | None = None,
        end_utime: int | None = None,
        start_lt: int | None = None,
        end_lt: int | None = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> TransactionsResponse:
        """Get transactions by specified filter.

        :param workchain: Block workchain.
        :param shard: Block shard id. Must be sent with *workchain*. Example: `8000000000000000`.
        :param seqno: Block seqno. Must be sent with *workchain* and *shard*.
        :param mc_seqno: Masterchain block seqno.
        :param account: List of account addresses to get transactions. Can be sent in hex, base64 or base64url form.
        :param exclude_account: Exclude transactions on specified account addresses.
        :param hash: Transaction hash.
        :param lt: Transaction lt.
        :param start_utime: Query transactions with generation UTC timestamp **after** given timestamp.
        :param end_utime: Query transactions with generation UTC timestamp **before** given timestamp.
        :param start_lt: Query transactions with `lt >= start_lt`.
        :param end_lt: Query transactions with `lt <= end_lt`.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort transactions by lt.
        :return: ``TransactionsResponse``.
        """
        path = "/transactions"
        params = {
            "workchain": workchain,
            "shard": shard,
            "seqno": seqno,
            "mc_seqno": mc_seqno,
            "account": account,
            "exclude_account": exclude_account,
            "hash": hash,
            "lt": lt,
            "start_utime": start_utime,
            "end_utime": end_utime,
            "start_lt": start_lt,
            "end_lt": end_lt,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=TransactionsResponse,
        )

    async def get_transactions_by_masterchain_block(
        self,
        seqno: int,
        limit: int = 10,
        offset: int = 0,
        sort: str = "desc",
    ) -> TransactionsResponse:
        """Return transactions from masterchain block and from all shards.

        :param seqno: Masterchain block seqno.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :param sort: Sort transactions by lt.
        :return: ``TransactionsResponse``.
        """
        path = "/transactionsByMasterchainBlock"
        params = {
            "seqno": seqno,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=TransactionsResponse,
        )

    async def get_transactions_by_message(
        self,
        msg_hash: str | None = None,
        body_hash: str | None = None,
        opcode: str | None = None,
        direction: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> TransactionsResponse:
        """Get transactions whose inbound/outbound message has the specified hash.

        :param msg_hash: Message hash. Acceptable in hex, base64 and base64url forms.
        :param body_hash: Hash of message body.
        :param opcode: Opcode of message in hex or signed 32-bit decimal form.
        :param direction: Direction of message.
        :param limit: Limit number of queried rows. Use with *offset* to batch read.
        :param offset: Skip first N rows. Use with *limit* to batch read.
        :return: ``TransactionsResponse``.
        """
        path = "/transactionsByMessage"
        params = {
            "msg_hash": msg_hash,
            "body_hash": body_hash,
            "opcode": opcode,
            "direction": direction,
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=TransactionsResponse,
        )
