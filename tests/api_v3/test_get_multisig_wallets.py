from toncenter.rest.v3.models import MultisigResponse


async def test_get_multisig_wallets(client):
    response = await client.v3.multisig.get_multisig_wallets(
        address=["UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"],
    )
    assert isinstance(response, MultisigResponse)
