from toncenter.rest.v2.models import BlockTransactions


async def test_get_block_transactions(client):
    response = await client.v2.transactions.get_block_transactions(
        -1,
        "-9223372036854775808",
        57981181,
    )
    assert isinstance(response, BlockTransactions)
