from toncenter.rest.v2.models import BlockSignatures


async def test_get_masterchain_block_signatures(client):
    response = await client.v2.blocks.get_masterchain_block_signatures(
        57981181,
    )
    assert isinstance(response, BlockSignatures)
