from toncenter.rest.v3.models import V2WalletInformation


async def test_get_wallet_information(client):
    response = await client.v3.api_v2.get_wallet_information(
        address="UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0",
    )
    assert isinstance(response, V2WalletInformation)
