from toncenter.rest.v3.models import TransactionsResponse


async def test_get_adjacent_transactions(client):
    response = await client.v3.blockchain.get_adjacent_transactions(
        hash="8085186e2c707c0de954e5456f065965988a01f7069bef6a6db32325af0e0d53",
    )
    assert isinstance(response, TransactionsResponse)
