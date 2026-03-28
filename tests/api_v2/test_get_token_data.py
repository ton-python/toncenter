from toncenter.rest.v2.models import JettonMasterData, JettonWalletData, NftCollectionData, NftItemData


async def test_get_token_data(client):
    response = await client.v2.accounts.get_token_data(
        "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
    )
    assert isinstance(response, (JettonMasterData, JettonWalletData, NftCollectionData, NftItemData))
