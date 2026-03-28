from toncenter.rest.v2.models import RunGetMethodStdResult


async def test_run_get_method_std(client):
    response = await client.v2.runmethod.run_get_method_std(
        "EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz",
        "dnsresolve",
        [
            {
                "@type": "tvm.stackEntrySlice",
                "slice": {
                    "@type": "tvm.slice",
                    "bytes": "te6ccgEBAQEABwAACm5lc3MA",
                },
            },
            {
                "@type": "tvm.stackEntryNumber",
                "number": {
                    "@type": "tvm.numberDecimal",
                    "number": "11610787539498642935599668790717661692618498088587845498754709837898668459007",
                },
            },
        ],
    )
    assert isinstance(response, RunGetMethodStdResult)
    assert response.exit_code == 0
