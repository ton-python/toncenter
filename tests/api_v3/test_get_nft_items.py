from toncenter.rest.v3.models import NFTItemsResponse


async def test_get_nft_items(client):
    response = await client.v3.nfts.get_nft_items(
        address=["EQAMrsze7MaG_7P2ENd1eeT-S2VttJ1myT9sX5f-F1gY7xGx"],
    )
    assert isinstance(response, NFTItemsResponse)
