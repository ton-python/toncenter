from toncenter.rest.v2.models import MasterchainInfo


async def test_get_masterchain_info(client):
    response = await client.v2.blocks.get_masterchain_info()
    assert isinstance(response, MasterchainInfo)
