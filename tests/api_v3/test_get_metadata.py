from toncenter.rest.v3.models import Metadata


async def test_get_metadata(client):
    response = await client.v3.accounts.get_metadata(
        address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    )
    assert isinstance(response, Metadata)
