from toncenter.rest.v3.models import TransactionsResponse


async def test_get_transactions_by_masterchain_block(client):
    response = await client.v3.blockchain.get_transactions_by_masterchain_block(
        seqno=57981181,
    )
    assert isinstance(response, TransactionsResponse)
