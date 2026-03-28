from toncenter.rest.v2.models import RunGetMethodResult


async def test_run_get_method(client):
    response = await client.v2.runmethod.run_get_method(
        "EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz",
        "dnsresolve",
        [
            ["tvm.Slice", "te6ccgEBAQEABwAACm5lc3MA"],
            ["num", "0x19f02441ee588fdb26ee24b2568dd035c3c9206e11ab979be62e55558a1d17ff"],
        ],
    )
    assert isinstance(response, RunGetMethodResult)
    assert response.exit_code == 0
