from toncenter.rest.v2.models import TonBlockIdExt


async def test_lookup_block(client):
    response = await client.v2.blocks.lookup_block(
        0,
        "-9223372036854775808",
        seqno=49560770,
    )
    assert isinstance(response, TonBlockIdExt)
