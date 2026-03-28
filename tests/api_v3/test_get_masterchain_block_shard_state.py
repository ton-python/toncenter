from toncenter.rest.v3.models import BlocksResponse


async def test_get_masterchain_block_shard_state(client):
    response = await client.v3.blockchain.get_masterchain_block_shard_state(
        seqno=57981181,
    )
    assert isinstance(response, BlocksResponse)
