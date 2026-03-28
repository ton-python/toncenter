from toncenter.rest.v3.models import V2RunGetMethodRequest, V2RunGetMethodResult, V2StackEntity


async def test_run_get_method(client):
    body = V2RunGetMethodRequest(
        address="EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz",
        method="dnsresolve",
        stack=[
            V2StackEntity(type="slice", value="te6ccgEBAQEABwAACm5lc3MA"),
            V2StackEntity(type="num", value="0x19f02441ee588fdb26ee24b2568dd035c3c9206e11ab979be62e55558a1d17ff"),
        ],
    )
    response = await client.v3.api_v2.run_get_method(body)
    assert isinstance(response, V2RunGetMethodResult)
    assert response.exit_code == 0
