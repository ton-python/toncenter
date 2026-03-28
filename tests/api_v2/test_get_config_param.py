from toncenter.rest.v2.models import ConfigInfo


async def test_get_config_param(client):
    response = await client.v2.configuration.get_config_param(
        0,
    )
    assert isinstance(response, ConfigInfo)
