from toncenter.rest.v3.models import TracesResponse


async def test_get_pending_traces(client):
    response = await client.v3.actions.get_pending_traces(
        account="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, TracesResponse)
