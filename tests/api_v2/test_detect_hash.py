from toncenter.rest.v2.models import DetectHash


async def test_detect_hash(client):
    response = await client.v2.utils.detect_hash(
        "8085186e2c707c0de954e5456f065965988a01f7069bef6a6db32325af0e0d53",
    )
    assert isinstance(response, DetectHash)
