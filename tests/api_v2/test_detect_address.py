from toncenter.rest.v2.models import DetectAddress


async def test_detect_address(client):
    response = await client.v2.utils.detect_address(
        "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, DetectAddress)
