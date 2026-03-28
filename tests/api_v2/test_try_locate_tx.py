from toncenter.rest.v2.models import Transaction


async def test_try_locate_tx(client):
    response = await client.v2.transactions.try_locate_tx(
        "EQAe8YtZ_XIHYK2An1R9xXIKedq3ghag2nX3PFScxcZQ_xHV",
        "EQBAjaOyi2wGWlk-EDkSabqqnF-MrrwMadnwqrurKpkla9nE",
        "68403494000002",
    )
    assert isinstance(response, Transaction)
