from toncenter.rest.v3.models import JettonBurnsResponse


async def test_get_jetton_burns(client):
    response = await client.v3.jettons.get_jetton_burns(
        jetton_master="EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
    )
    assert isinstance(response, JettonBurnsResponse)
