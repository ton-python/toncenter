from toncenter.rest.v3.models import NFTTransfersResponse


async def test_get_nft_transfers(client):
    response = await client.v3.nfts.get_nft_transfers(
        collection_address="EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz",
    )
    assert isinstance(response, NFTTransfersResponse)
