from toncenter.rest.v3.models import BlocksResponse


async def test_get_blocks(client):
    response = await client.v3.blockchain.get_blocks()
    assert isinstance(response, BlocksResponse)
