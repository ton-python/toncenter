from toncenter.rest.v3.models import MultisigOrderResponse


async def test_get_multisig_orders(client):
    response = await client.v3.multisig.get_multisig_orders(
        multisig_address=["UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"],
    )
    assert isinstance(response, MultisigOrderResponse)
