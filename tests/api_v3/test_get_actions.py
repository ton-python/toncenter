from toncenter.rest.v3.models import ActionsResponse


async def test_get_actions(client):
    response = await client.v3.actions.get_actions(
        account="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, ActionsResponse)
