from toncenter.rest.v3.models import MessagesResponse


async def test_get_messages(client):
    response = await client.v3.blockchain.get_messages(
        msg_hash=["4eee803beab5a31685b5c06a0716bd770f662db0395acbebc2ee6dd9c8227c34"],
    )
    assert isinstance(response, MessagesResponse)
