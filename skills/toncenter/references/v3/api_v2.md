# V3 API V2

5 methods from `client.v3.api_v2` — V2 methods available through the V3 endpoint.

## get_address_information

Get account information via V3 endpoint.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| use_v2 | bool | no | True | Use method from api/v2 (not recommended) |

Returns: `V2AddressInformation`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 api_v2 get_address_information --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v3.api_v2.get_address_information(
    address="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
)
```

## estimate_fee

Estimate fee via V3 endpoint. Accepts a request body object.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | `V2EstimateFeeRequest` | yes | — | Request body |

`V2EstimateFeeRequest` fields:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| address | str \| None | None | Destination address |
| body | str \| None | None | Base64-encoded message body |
| ignore_chksig | bool \| None | None | Skip signature check |
| init_code | str \| None | None | Base64-encoded init code |
| init_data | str \| None | None | Base64-encoded init data |

Returns: `V2EstimateFeeResult`

```python
from toncenter.rest.v3.models import V2EstimateFeeRequest

result = await client.v3.api_v2.estimate_fee(
    body=V2EstimateFeeRequest(
        address="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
        body="te6cck...",
    ),
)
```

## send_message

Send a message via V3 endpoint. Accepts a request body object.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | `V2SendMessageRequest` | yes | — | Request body |

`V2SendMessageRequest` fields:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| boc | str \| None | None | Base64-encoded serialized BoC |

Returns: `V2SendMessageResult`

```python
from toncenter.rest.v3.models import V2SendMessageRequest

result = await client.v3.api_v2.send_message(
    body=V2SendMessageRequest(boc="te6cck..."),
)
```

## run_get_method

Run a smart contract get-method via V3 endpoint. Accepts a request body object.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | `V2RunGetMethodRequest` | yes | — | Request body |

`V2RunGetMethodRequest` fields:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| address | str \| None | None | Smart contract address |
| method | str \| None | None | Method name |
| stack | list[`V2StackEntity`] \| None | None | Stack entries |

`V2StackEntity` fields: `type: str | None`, `value: Any | None`. Types: "num", "cell", "slice".

Returns: `V2RunGetMethodResult`

```python
from toncenter.rest.v3.models import V2RunGetMethodRequest, V2StackEntity

result = await client.v3.api_v2.run_get_method(
    body=V2RunGetMethodRequest(
        address="EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
        method="get_jetton_data",
    ),
)
```

## get_wallet_information

Get wallet information via V3 endpoint.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| address | str | yes | — | Account address in any form |
| use_v2 | bool | no | True | Use method from api/v2 (not recommended) |

Supported wallets: v1r1, v1r2, v1r3, v2r1, v2r2, v3r1, v3r2, v4r1, v4r2, v5beta, v5r1. Returns 409 if not a wallet.

Returns: `V2WalletInformation`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py v3 api_v2 get_wallet_information --address EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2
```

```python
result = await client.v3.api_v2.get_wallet_information(
    address="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
)
```
