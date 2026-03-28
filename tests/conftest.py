import pytest
from environs import Env

from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

env = Env()
env.read_env()

API_KEY = env.str("TONCENTER_API_KEY")
NETWORK = Network[env.str("TONCENTER_NETWORK", "mainnet").upper()]
RPS_LIMIT = env.int("TONCENTER_RPS_LIMIT")
RPS_PERIOD = env.float("TONCENTER_RPS_PERIOD")


@pytest.fixture
async def client():
    c = ToncenterRestClient(
        API_KEY,
        NETWORK,
        rps_limit=RPS_LIMIT,
        rps_period=RPS_PERIOD,
    )
    await c.create_session()
    yield c
    await c.close_session()
