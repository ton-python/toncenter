from toncenter.rest.v3.models import AddressBook


async def test_get_address_book(client):
    response = await client.v3.accounts.get_address_book(
        address=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
    )
    assert isinstance(response, AddressBook)
