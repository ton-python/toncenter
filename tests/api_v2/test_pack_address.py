async def test_pack_address(client):
    response = await client.v2.utils.pack_address(
        "0:ed169130705004711b9b98b561d8de82d31fbf84910ced6eb5fc92e7485ef8a7",
    )
    assert isinstance(response, str)
