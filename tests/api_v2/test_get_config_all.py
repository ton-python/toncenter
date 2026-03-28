from toncenter.rest.v2.models import ConfigInfo


async def test_get_config_all(client):
    response = await client.v2.configuration.get_config_all()
    assert isinstance(response, ConfigInfo)
