from toncenter.rest.v2.models import ShardBlockProof


async def test_get_shard_block_proof(client):
    response = await client.v2.blocks.get_shard_block_proof(
        0,
        "-9223372036854775808",
        49560770,
    )
    assert isinstance(response, ShardBlockProof)
