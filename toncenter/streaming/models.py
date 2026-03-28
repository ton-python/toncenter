import typing as t
from enum import Enum

from pydantic import BaseModel, Field


class ConnectionState(str, Enum):
    """Streaming transport connection state."""

    IDLE = "idle"
    CONNECTING = "connecting"
    SUBSCRIBED = "subscribed"
    RECONNECTING = "reconnecting"


class Finality(str, Enum):
    """Finality level of a streaming notification.

    Lifecycle: ``pending`` → ``confirmed`` → ``finalized``.
    """

    PENDING = "pending"
    CONFIRMED = "confirmed"
    FINALIZED = "finalized"


class EventType(str, Enum):
    """Streaming notification type identifiers.

    The first five values are used in the ``types`` subscription parameter.
    ``TRACE_INVALIDATED`` is a server-only notification type that cannot
    be subscribed to directly — it is emitted automatically when a
    previously-reported trace becomes invalid.
    """

    TRANSACTIONS = "transactions"
    ACTIONS = "actions"
    TRACE = "trace"
    ACCOUNT_STATE_CHANGE = "account_state_change"
    JETTONS_CHANGE = "jettons_change"
    TRACE_INVALIDATED = "trace_invalidated"


class ActionType(str, Enum):
    """Well-known action type identifiers.

    Used in the ``action_types`` subscription filter.
    """

    CALL_CONTRACT = "call_contract"
    CONTRACT_DEPLOY = "contract_deploy"
    TON_TRANSFER = "ton_transfer"
    AUCTION_BID = "auction_bid"
    CHANGE_DNS = "change_dns"
    DEX_DEPOSIT_LIQUIDITY = "dex_deposit_liquidity"
    DEX_WITHDRAW_LIQUIDITY = "dex_withdraw_liquidity"
    DELETE_DNS = "delete_dns"
    RENEW_DNS = "renew_dns"
    ELECTION_DEPOSIT = "election_deposit"
    ELECTION_RECOVER = "election_recover"
    JETTON_BURN = "jetton_burn"
    JETTON_SWAP = "jetton_swap"
    JETTON_TRANSFER = "jetton_transfer"
    JETTON_MINT = "jetton_mint"
    NFT_MINT = "nft_mint"
    TICK_TOCK = "tick_tock"
    STAKE_DEPOSIT = "stake_deposit"
    STAKE_WITHDRAWAL = "stake_withdrawal"
    STAKE_WITHDRAWAL_REQUEST = "stake_withdrawal_request"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"


class AccountState(BaseModel):
    """Account state snapshot from ``account_state_change`` notification."""

    hash: str | None = None
    balance: str | None = None
    account_status: str | None = None
    data_hash: str | None = None
    code_hash: str | None = None


class JettonWallet(BaseModel):
    """Jetton wallet snapshot from ``jettons_change`` notification."""

    address: str | None = None
    balance: str | None = None
    owner: str | None = None
    jetton: str | None = None
    last_transaction_lt: str | None = None


class _FinalityMixin:
    """Mixin providing finality convenience properties."""

    finality: str

    @property
    def is_pending(self) -> bool:
        """Return ``True`` if finality is ``pending``."""
        return self.finality == Finality.PENDING

    @property
    def is_confirmed(self) -> bool:
        """Return ``True`` if finality is ``confirmed``."""
        return self.finality == Finality.CONFIRMED

    @property
    def is_finalized(self) -> bool:
        """Return ``True`` if finality is ``finalized``."""
        return self.finality == Finality.FINALIZED


class TransactionsNotification(_FinalityMixin, BaseModel):
    """Transactions notification."""

    type: t.Literal["transactions"] = "transactions"
    finality: str
    trace_external_hash_norm: str
    transactions: list[dict[str, t.Any]] = Field(default_factory=list)
    address_book: dict[str, t.Any] | None = None
    metadata: dict[str, t.Any] | None = None


class ActionsNotification(_FinalityMixin, BaseModel):
    """Actions notification."""

    type: t.Literal["actions"] = "actions"
    finality: str
    trace_external_hash_norm: str
    actions: list[dict[str, t.Any]] = Field(default_factory=list)
    address_book: dict[str, t.Any] | None = None
    metadata: dict[str, t.Any] | None = None


class TraceNotification(_FinalityMixin, BaseModel):
    """Trace notification."""

    type: t.Literal["trace"] = "trace"
    finality: str
    trace_external_hash_norm: str
    trace: dict[str, t.Any] | None = None
    transactions: dict[str, t.Any] | None = None
    actions: list[dict[str, t.Any]] | None = None
    address_book: dict[str, t.Any] | None = None
    metadata: dict[str, t.Any] | None = None


class AccountStateNotification(_FinalityMixin, BaseModel):
    """Account state change notification."""

    type: t.Literal["account_state_change"] = "account_state_change"
    finality: str
    account: str
    state: AccountState | None = None


class JettonsNotification(_FinalityMixin, BaseModel):
    """Jettons change notification."""

    type: t.Literal["jettons_change"] = "jettons_change"
    finality: str
    jetton: JettonWallet | None = None
    address_book: dict[str, t.Any] | None = None
    metadata: dict[str, t.Any] | None = None


class TraceInvalidatedNotification(BaseModel):
    """Trace invalidated notification.

    Clients must discard any cached trace/transactions/actions
    for the given ``trace_external_hash_norm``.
    """

    type: t.Literal["trace_invalidated"] = "trace_invalidated"
    trace_external_hash_norm: str


StreamNotification: t.TypeAlias = (
    TransactionsNotification
    | ActionsNotification
    | TraceNotification
    | AccountStateNotification
    | JettonsNotification
    | TraceInvalidatedNotification
)

NOTIFICATION_MODEL_MAP: t.Final[dict[str, type[BaseModel]]] = {
    "transactions": TransactionsNotification,
    "actions": ActionsNotification,
    "trace": TraceNotification,
    "account_state_change": AccountStateNotification,
    "jettons_change": JettonsNotification,
    "trace_invalidated": TraceInvalidatedNotification,
}
