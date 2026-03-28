import pytest

from toncenter.exceptions import ToncenterNotFoundError
from toncenter.rest.v3.models import TransactionsResponse


async def test_get_pending_transactions(client):
    try:
        response = await client.v3.blockchain.get_pending_transactions(
            account=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
        )
        assert isinstance(response, TransactionsResponse)
    except ToncenterNotFoundError:
        pytest.skip("No pending transactions at the moment")
