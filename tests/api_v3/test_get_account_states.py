from toncenter.rest.v3.models import AccountStatesResponse


async def test_get_account_states(client):
    response = await client.v3.accounts.get_account_states(
        address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    )
    assert isinstance(response, AccountStatesResponse)
