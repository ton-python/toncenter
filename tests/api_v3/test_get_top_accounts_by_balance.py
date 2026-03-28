from toncenter.rest.v3.models import AccountBalance


async def test_get_top_accounts_by_balance(client):
    response = await client.v3.stats.get_top_accounts_by_balance()
    assert isinstance(response, list)
    assert len(response) > 0
    assert all(isinstance(item, AccountBalance) for item in response)
