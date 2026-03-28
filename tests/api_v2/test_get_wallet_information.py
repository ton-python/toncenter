from toncenter.rest.v2.models import WalletInformation


async def test_get_wallet_information(client):
    response = await client.v2.accounts.get_wallet_information(
        "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0",
    )
    assert isinstance(response, WalletInformation)
