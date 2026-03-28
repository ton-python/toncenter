from toncenter.rest.v2.models import BlockHeader


async def test_get_block_header(client):
    response = await client.v2.blocks.get_block_header(
        0,
        "-9223372036854775808",
        49560770,
    )
    assert isinstance(response, BlockHeader)
