from toncenter.rest.v3.models import JettonMastersResponse


async def test_get_jetton_masters(client):
    response = await client.v3.jettons.get_jetton_masters(
        address=["EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs"],
    )
    assert isinstance(response, JettonMastersResponse)
