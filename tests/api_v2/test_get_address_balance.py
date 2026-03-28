async def test_get_address_balance(client):
    response = await client.v2.accounts.get_address_balance(
        "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, str)
