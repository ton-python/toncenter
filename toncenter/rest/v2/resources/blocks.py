from __future__ import annotations

import typing as t

from toncenter.rest.v2.models import (
    BlockHeader,
    BlockSignatures,
    ConsensusBlock,
    MasterchainInfo,
    OutMsgQueueSizes,
    ShardBlockProof,
    Shards,
    TonBlockIdExt,
)
from toncenter.rest.v2.resources._base import BaseResource


class BlocksResource(BaseResource):
    """Access masterchain and shard block information."""

    async def get_masterchain_info(self) -> MasterchainInfo:
        """Get current masterchain state.

        :return: ``MasterchainInfo``.
        """
        return await self._request(
            "GET",
            "/getMasterchainInfo",
            response_model=MasterchainInfo,
        )

    async def get_masterchain_block_signatures(self, seqno: int) -> BlockSignatures:
        """Get validator signatures for a masterchain block.

        :param seqno: Masterchain block sequence number.
        :return: ``BlockSignatures``.
        """
        return await self._request(
            "GET",
            "/getMasterchainBlockSignatures",
            params={"seqno": seqno},
            response_model=BlockSignatures,
        )

    async def get_shard_block_proof(
        self,
        workchain: int,
        shard: str,
        seqno: int,
        *,
        from_seqno: int | None = None,
    ) -> ShardBlockProof:
        """Get merkle proof of a shard block.

        :param workchain: Workchain ID.
        :param shard: Shard ID.
        :param seqno: Block sequence number.
        :param from_seqno: Starting masterchain seqno for proof chain.
        :return: ``ShardBlockProof``.
        """
        params: dict[str, t.Any] = {
            "workchain": workchain,
            "shard": shard,
            "seqno": seqno,
        }
        if from_seqno is not None:
            params["from_seqno"] = from_seqno
        return await self._request(
            "GET",
            "/getShardBlockProof",
            params=params,
            response_model=ShardBlockProof,
        )

    async def get_consensus_block(self) -> ConsensusBlock:
        """Get block number confirmed by validator consensus.

        :return: ``ConsensusBlock``.
        """
        return await self._request(
            "GET",
            "/getConsensusBlock",
            response_model=ConsensusBlock,
        )

    async def lookup_block(
        self,
        workchain: int,
        shard: str,
        *,
        seqno: int | None = None,
        lt: str | None = None,
        unixtime: int | None = None,
    ) -> TonBlockIdExt:
        """Look up a block by workchain/shard and either seqno, lt, or time.

        :param workchain: Workchain ID.
        :param shard: Shard ID.
        :param seqno: Block sequence number.
        :param lt: Logical time.
        :param unixtime: UNIX timestamp.
        :return: ``TonBlockIdExt``.
        """
        params: dict[str, t.Any] = {"workchain": workchain, "shard": shard}
        if seqno is not None:
            params["seqno"] = seqno
        if lt is not None:
            params["lt"] = lt
        if unixtime is not None:
            params["unixtime"] = unixtime
        return await self._request(
            "GET",
            "/lookupBlock",
            params=params,
            response_model=TonBlockIdExt,
        )

    async def get_shards(self, seqno: int) -> Shards:
        """Get shard descriptors for a masterchain block.

        :param seqno: Masterchain block sequence number.
        :return: ``Shards``.
        """
        return await self._request(
            "GET",
            "/getShards",
            params={"seqno": seqno},
            response_model=Shards,
        )

    async def get_block_header(
        self,
        workchain: int,
        shard: str,
        seqno: int,
        *,
        root_hash: str | None = None,
        file_hash: str | None = None,
    ) -> BlockHeader:
        """Get block header information.

        :param workchain: Workchain ID.
        :param shard: Shard ID.
        :param seqno: Block sequence number.
        :param root_hash: Optional root hash for verification.
        :param file_hash: Optional file hash for verification.
        :return: ``BlockHeader``.
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
        return await self._request(
            "GET",
            "/getBlockHeader",
            params=params,
            response_model=BlockHeader,
        )

    async def get_out_msg_queue_size(self) -> OutMsgQueueSizes:
        """Get outbound message queue sizes across all shards.

        :return: ``OutMsgQueueSizes``.
        """
        return await self._request(
            "GET",
            "/getOutMsgQueueSize",
            response_model=OutMsgQueueSizes,
        )
