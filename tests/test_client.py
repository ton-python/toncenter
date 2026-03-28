import pytest

from toncenter.exceptions import (
    ToncenterBadRequestError,
    ToncenterInternalServerError,
    ToncenterNotFoundError,
    ToncenterSessionError,
    ToncenterUnauthorizedError,
    ToncenterUnprocessableError,
)
from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

ADDRESS = "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"


async def test_session_not_created():
    c = ToncenterRestClient("fake-key", Network.MAINNET)
    with pytest.raises(ToncenterSessionError):
        await c.v2.accounts.get_address_information(
            ADDRESS,
        )


async def test_session_context_manager():
    c = ToncenterRestClient("fake-key", Network.MAINNET)
    async with c:
        assert c._session is not None
        assert not c._session.closed
    assert c._session is None


async def test_close_session_idempotent():
    c = ToncenterRestClient("fake-key", Network.MAINNET)
    await c.create_session()
    await c.close_session()
    await c.close_session()


async def test_invalid_api_key():
    c = ToncenterRestClient("invalid-key-12345", Network.MAINNET)
    await c.create_session()
    try:
        with pytest.raises(ToncenterUnauthorizedError):
            await c.v2.accounts.get_address_information(
                ADDRESS,
            )
    finally:
        await c.close_session()


async def test_retry_policy_disabled():
    c = ToncenterRestClient("invalid-key", Network.MAINNET, retry_policy=None)
    await c.create_session()
    try:
        with pytest.raises(ToncenterUnauthorizedError):
            await c.v2.accounts.get_address_information(
                ADDRESS,
            )
    finally:
        await c.close_session()


async def test_v2_invalid_address(client):
    with pytest.raises((ToncenterBadRequestError, ToncenterUnprocessableError)):
        await client.v2.accounts.get_address_information(
            "not-a-valid-address",
        )


async def test_v3_invalid_address(client):
    with pytest.raises((ToncenterBadRequestError, ToncenterUnprocessableError)):
        await client.v3.accounts.get_account_states(
            address=["not-a-valid-address"],
        )


async def test_v2_not_found(client):
    with pytest.raises((ToncenterNotFoundError, ToncenterInternalServerError)):
        await client.v2.transactions.try_locate_tx(
            ADDRESS,
            ADDRESS,
            "1",
        )
