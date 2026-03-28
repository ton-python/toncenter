from __future__ import annotations

import typing as t

from toncenter.rest.v2.resources.accounts import AccountsResource
from toncenter.rest.v2.resources.blocks import BlocksResource
from toncenter.rest.v2.resources.configuration import ConfigurationResource
from toncenter.rest.v2.resources.rpc import RpcResource
from toncenter.rest.v2.resources.runmethod import RunmethodResource
from toncenter.rest.v2.resources.send import SendResource
from toncenter.rest.v2.resources.transactions import TransactionsResource
from toncenter.rest.v2.resources.utils import UtilsResource

if t.TYPE_CHECKING:
    from toncenter.rest.client import ToncenterRestClient


class V2Mixin:
    """Mixin that exposes all API v2 resources as properties."""

    def __init__(self, client: ToncenterRestClient) -> None:
        self._client = client
        self._accounts = AccountsResource(client)
        self._blocks = BlocksResource(client)
        self._configuration = ConfigurationResource(client)
        self._rpc = RpcResource(client)
        self._runmethod = RunmethodResource(client)
        self._send = SendResource(client)
        self._transactions = TransactionsResource(client)
        self._utils = UtilsResource(client)

    @property
    def accounts(self) -> AccountsResource:
        """Access ``AccountsResource`` resource group."""
        return self._accounts

    @property
    def blocks(self) -> BlocksResource:
        """Access ``BlocksResource`` resource group."""
        return self._blocks

    @property
    def configuration(self) -> ConfigurationResource:
        """Access ``ConfigurationResource`` resource group."""
        return self._configuration

    @property
    def rpc(self) -> RpcResource:
        """Access ``RpcResource`` resource group."""
        return self._rpc

    @property
    def runmethod(self) -> RunmethodResource:
        """Access ``RunmethodResource`` resource group."""
        return self._runmethod

    @property
    def send(self) -> SendResource:
        """Access ``SendResource`` resource group."""
        return self._send

    @property
    def transactions(self) -> TransactionsResource:
        """Access ``TransactionsResource`` resource group."""
        return self._transactions

    @property
    def utils(self) -> UtilsResource:
        """Access ``UtilsResource`` resource group."""
        return self._utils
