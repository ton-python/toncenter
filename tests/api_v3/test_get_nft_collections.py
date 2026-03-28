from toncenter.rest.v3.models import NFTCollectionsResponse


async def test_get_nft_collections(client):
    response = await client.v3.nfts.get_nft_collections(
        collection_address=["EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz"],
    )
    assert isinstance(response, NFTCollectionsResponse)
