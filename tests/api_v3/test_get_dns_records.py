from toncenter.rest.v3.models import DNSRecordsResponse


async def test_get_dns_records(client):
    response = await client.v3.dns.get_dns_records(
        domain="ness.ton",
    )
    assert isinstance(response, DNSRecordsResponse)
