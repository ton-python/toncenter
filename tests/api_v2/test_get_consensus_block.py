from toncenter.rest.v2.models import ConsensusBlock


async def test_get_consensus_block(client):
    response = await client.v2.blocks.get_consensus_block()
    assert isinstance(response, ConsensusBlock)
