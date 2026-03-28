async def test_unpack_address(client):
    response = await client.v2.utils.unpack_address(
        "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, str)
