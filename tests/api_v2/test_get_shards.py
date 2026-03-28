from toncenter.rest.v2.models import Shards


async def test_get_shards(client):
    response = await client.v2.blocks.get_shards(
        57981181,
    )
    assert isinstance(response, Shards)
