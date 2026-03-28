from toncenter.rest.v2.models import ExtendedAddressInformation


async def test_get_extended_address_information(client):
    response = await client.v2.accounts.get_extended_address_information(
        "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, ExtendedAddressInformation)
