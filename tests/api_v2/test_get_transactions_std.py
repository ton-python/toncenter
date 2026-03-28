from toncenter.rest.v2.models import TransactionsStd


async def test_get_transactions_std(client):
    response = await client.v2.transactions.get_transactions_std(
        "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
    )
    assert isinstance(response, TransactionsStd)
