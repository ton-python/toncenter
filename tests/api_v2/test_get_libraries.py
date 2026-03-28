from toncenter.rest.v2.models import LibraryResult


async def test_get_libraries(client):
    response = await client.v2.configuration.get_libraries(
        ["8F452D7A4DFD74066B682365177259ED05734435BE76B5FD4BD5D8AF2B7C3D68"],
    )
    assert isinstance(response, LibraryResult)
