from toncenter.rest.v2.models import BlockTransactionsExt


async def test_get_block_transactions_ext(client):
    response = await client.v2.transactions.get_block_transactions_ext(
        -1,
        "-9223372036854775808",
        57981181,
    )
    assert isinstance(response, BlockTransactionsExt)
