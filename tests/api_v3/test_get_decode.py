from toncenter.rest.v3.models import DecodeResponse


async def test_get_decode(client):
    response = await client.v3.utils.get_decode(
        opcodes=["0x0f8a7ea5"],
    )
    assert isinstance(response, DecodeResponse)
