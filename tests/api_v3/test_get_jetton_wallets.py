from toncenter.rest.v3.models import JettonWalletsResponse


async def test_get_jetton_wallets(client):
    response = await client.v3.jettons.get_jetton_wallets(
        owner_address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    )
    assert isinstance(response, JettonWalletsResponse)
