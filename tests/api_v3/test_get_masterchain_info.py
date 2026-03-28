from toncenter.rest.v3.models import MasterchainInfo


async def test_get_masterchain_info(client):
    response = await client.v3.blockchain.get_masterchain_info()
    assert isinstance(response, MasterchainInfo)
