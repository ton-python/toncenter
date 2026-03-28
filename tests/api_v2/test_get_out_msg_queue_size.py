from toncenter.rest.v2.models import OutMsgQueueSizes


async def test_get_out_msg_queue_size(client):
    response = await client.v2.blocks.get_out_msg_queue_size()
    assert isinstance(response, OutMsgQueueSizes)
