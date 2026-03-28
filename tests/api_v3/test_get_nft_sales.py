from toncenter.rest.v3.models import NFTSalesResponse


async def test_get_nft_sales(client):
    response = await client.v3.nfts.get_nft_sales(
        address=["EQAMrsze7MaG_7P2ENd1eeT-S2VttJ1myT9sX5f-F1gY7xGx"],
    )
    assert isinstance(response, NFTSalesResponse)
