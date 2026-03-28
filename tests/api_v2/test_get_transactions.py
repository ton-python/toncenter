from toncenter.rest.v2.models import Transaction


async def test_get_transactions(client):
    response = await client.v2.transactions.get_transactions(
        "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, list)
    assert len(response) > 0
    assert all(isinstance(item, Transaction) for item in response)
