from toncenter.rest.v3.models import VestingContractsResponse


async def test_get_vesting_contracts(client):
    response = await client.v3.vesting.get_vesting_contracts(
        wallet_address=["UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"],
    )
    assert isinstance(response, VestingContractsResponse)
