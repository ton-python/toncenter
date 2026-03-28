from toncenter.rest.v3.models import WalletStatesResponse


async def test_get_wallet_states(client):
    response = await client.v3.accounts.get_wallet_states(
        address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    )
    assert isinstance(response, WalletStatesResponse)
