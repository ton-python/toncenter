from __future__ import annotations

import typing as t

from toncenter.rest.v3.resources.accounts import AccountsResource
from toncenter.rest.v3.resources.actions import ActionsResource
from toncenter.rest.v3.resources.api_v2 import ApiV2Resource
from toncenter.rest.v3.resources.blockchain import BlockchainResource
from toncenter.rest.v3.resources.dns import DnsResource
from toncenter.rest.v3.resources.jettons import JettonsResource
from toncenter.rest.v3.resources.multisig import MultisigResource
from toncenter.rest.v3.resources.nfts import NftsResource
from toncenter.rest.v3.resources.stats import StatsResource
from toncenter.rest.v3.resources.utils import UtilsResource
from toncenter.rest.v3.resources.vesting import VestingResource

if t.TYPE_CHECKING:
    from toncenter.rest.client import ToncenterRestClient


class V3Mixin:
    """Mixin that exposes all API v3 resources as properties."""

    def __init__(self, client: ToncenterRestClient) -> None:
        self._client = client
        self._accounts = AccountsResource(client)
        self._actions = ActionsResource(client)
        self._api_v2 = ApiV2Resource(client)
        self._blockchain = BlockchainResource(client)
        self._dns = DnsResource(client)
        self._jettons = JettonsResource(client)
        self._multisig = MultisigResource(client)
        self._nfts = NftsResource(client)
        self._stats = StatsResource(client)
        self._utils = UtilsResource(client)
        self._vesting = VestingResource(client)

    @property
    def accounts(self) -> AccountsResource:
        """Access ``AccountsResource`` resource group."""
        return self._accounts

    @property
    def actions(self) -> ActionsResource:
        """Access ``ActionsResource`` resource group."""
        return self._actions

    @property
    def api_v2(self) -> ApiV2Resource:
        """Access ``ApiV2Resource`` resource group."""
        return self._api_v2

    @property
    def blockchain(self) -> BlockchainResource:
        """Access ``BlockchainResource`` resource group."""
        return self._blockchain

    @property
    def dns(self) -> DnsResource:
        """Access ``DnsResource`` resource group."""
        return self._dns

    @property
    def jettons(self) -> JettonsResource:
        """Access ``JettonsResource`` resource group."""
        return self._jettons

    @property
    def multisig(self) -> MultisigResource:
        """Access ``MultisigResource`` resource group."""
        return self._multisig

    @property
    def nfts(self) -> NftsResource:
        """Access ``NftsResource`` resource group."""
        return self._nfts

    @property
    def stats(self) -> StatsResource:
        """Access ``StatsResource`` resource group."""
        return self._stats

    @property
    def utils(self) -> UtilsResource:
        """Access ``UtilsResource`` resource group."""
        return self._utils

    @property
    def vesting(self) -> VestingResource:
        """Access ``VestingResource`` resource group."""
        return self._vesting
