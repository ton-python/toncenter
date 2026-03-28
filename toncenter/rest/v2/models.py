from __future__ import annotations

import typing as t
from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class ToncenterModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class TonlibModel(ToncenterModel):
    type: str | None = Field(default=None, alias="@type")


class AccountStateEnum(str, Enum):
    UNINITIALIZED = "uninitialized"
    ACTIVE = "active"
    FROZEN = "frozen"


class TonBlockIdExt(TonlibModel):
    workchain: int
    shard: str
    seqno: int
    root_hash: str
    file_hash: str


class AccountAddress(TonlibModel):
    account_address: str


class InternalTransactionId(TonlibModel):
    lt: str
    hash: str


class ExtraCurrencyBalance(TonlibModel):
    id: int
    amount: str


class SmcAddr(TonlibModel):
    type: Literal["addr_std"] = Field(default="addr_std", alias="@type")
    workchain_id: int
    address: str


class RWalletLimit(TonlibModel):
    type: Literal["rwallet.limit"] = Field(default="rwallet.limit", alias="@type")
    seconds: int
    value: int


class RWalletConfig(TonlibModel):
    type: Literal["rwallet.config"] = Field(default="rwallet.config", alias="@type")
    start_at: int
    limits: list[RWalletLimit]


class PChanConfig(TonlibModel):
    type: Literal["pchan.config"] = Field(default="pchan.config", alias="@type")
    alice_public_key: str
    alice_address: AccountAddress
    bob_public_key: str
    bob_address: AccountAddress
    init_timeout: int
    close_timeout: int
    channel_id: int


class PChanStateInit(TonlibModel):
    type: Literal["pchan.stateInit"] = Field(default="pchan.stateInit", alias="@type")
    signed_A: bool
    signed_B: bool
    min_A: int
    min_B: int
    expire_at: int
    A: int
    B: int


class PChanStateClose(TonlibModel):
    type: Literal["pchan.stateClose"] = Field(default="pchan.stateClose", alias="@type")
    signed_A: bool
    signed_B: bool
    min_A: int
    min_B: int
    expire_at: int
    A: int
    B: int


class PChanStatePayout(TonlibModel):
    type: Literal["pchan.statePayout"] = Field(default="pchan.statePayout", alias="@type")
    A: int
    B: int


PChanState = Annotated[
    PChanStateInit | PChanStateClose | PChanStatePayout,
    Field(discriminator="type"),
]


class AccountStateRaw(TonlibModel):
    type: Literal["raw.accountState"] = Field(default="raw.accountState", alias="@type")
    code: str
    data: str
    frozen_hash: str


class AccountStateWalletV3(TonlibModel):
    type: Literal["wallet.v3.accountState"] = Field(
        default="wallet.v3.accountState",
        alias="@type",
    )
    wallet_id: int
    seqno: int


class AccountStateWalletV4(TonlibModel):
    type: Literal["wallet.v4.accountState"] = Field(
        default="wallet.v4.accountState",
        alias="@type",
    )
    wallet_id: int
    seqno: int


class AccountStateWalletHighloadV1(TonlibModel):
    type: Literal["wallet.highload.v1.accountState"] = Field(
        default="wallet.highload.v1.accountState",
        alias="@type",
    )
    wallet_id: int
    seqno: int


class AccountStateWalletHighloadV2(TonlibModel):
    type: Literal["wallet.highload.v2.accountState"] = Field(
        default="wallet.highload.v2.accountState",
        alias="@type",
    )
    wallet_id: int


class AccountStateDns(TonlibModel):
    type: Literal["dns.accountState"] = Field(default="dns.accountState", alias="@type")
    wallet_id: int


class AccountStateRWallet(TonlibModel):
    type: Literal["rwallet.accountState"] = Field(
        default="rwallet.accountState",
        alias="@type",
    )
    wallet_id: int
    seqno: int
    unlocked_balance: int
    config: RWalletConfig


class AccountStatePChan(TonlibModel):
    type: Literal["pchan.accountState"] = Field(
        default="pchan.accountState",
        alias="@type",
    )
    config: PChanConfig
    state: PChanState
    description: str


class AccountStateUninited(TonlibModel):
    type: Literal["uninited.accountState"] = Field(
        default="uninited.accountState",
        alias="@type",
    )
    frozen_hash: str


AccountState = Annotated[
    AccountStateRaw
    | AccountStateWalletV3
    | AccountStateWalletV4
    | AccountStateWalletHighloadV1
    | AccountStateWalletHighloadV2
    | AccountStateDns
    | AccountStateRWallet
    | AccountStatePChan
    | AccountStateUninited,
    Field(discriminator="type"),
]


class DnsRecordSmcAddress(TonlibModel):
    type: Literal["dns_smc_address"] = Field(default="dns_smc_address", alias="@type")
    smc_addr: SmcAddr


class DnsRecordNextResolver(TonlibModel):
    type: Literal["dns_next_resolver"] = Field(
        default="dns_next_resolver",
        alias="@type",
    )
    resolver: SmcAddr


class DnsRecordAdnlAddress(TonlibModel):
    type: Literal["dns_adnl_address"] = Field(
        default="dns_adnl_address",
        alias="@type",
    )
    adnl_addr: str


class DnsRecordStorageAddress(TonlibModel):
    type: Literal["dns_storage_address"] = Field(
        default="dns_storage_address",
        alias="@type",
    )
    bag_id: str


DnsRecord = Annotated[
    DnsRecordSmcAddress | DnsRecordNextResolver | DnsRecordAdnlAddress | DnsRecordStorageAddress,
    Field(discriminator="type"),
]


class DnsRecordSet(ToncenterModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    dns_next_resolver: DnsRecord | None = None
    wallet: DnsRecord | None = None
    site: DnsRecord | None = None
    storage: DnsRecord | None = None


class DnsContent(ToncenterModel):
    domain: str
    data: DnsRecordSet


class AddressInformation(TonlibModel):
    balance: str
    extra_currencies: list[ExtraCurrencyBalance]
    last_transaction_id: InternalTransactionId
    block_id: TonBlockIdExt
    code: str
    data: str
    frozen_hash: str
    sync_utime: int
    state: AccountStateEnum
    suspended: bool | None = None


class WalletInformation(TonlibModel):
    wallet: bool
    balance: str
    account_state: AccountStateEnum
    last_transaction_id: InternalTransactionId
    wallet_type: str | None = None
    seqno: int | None = None
    wallet_id: int | None = None
    is_signature_allowed: bool | None = None


class ExtendedAddressInformation(TonlibModel):
    address: AccountAddress
    balance: str
    extra_currencies: list[ExtraCurrencyBalance]
    last_transaction_id: InternalTransactionId
    block_id: TonBlockIdExt
    sync_utime: int
    account_state: AccountState
    revision: int


class MasterchainInfo(TonlibModel):
    last: TonBlockIdExt
    state_root_hash: str
    init: TonBlockIdExt


class ConsensusBlock(TonlibModel):
    consensus_block: int
    timestamp: int


class BlockSignature(TonlibModel):
    node_id_short: str
    signature: str


class BlockSignatures(TonlibModel):
    id: TonBlockIdExt
    signatures: list[BlockSignature]


class BlockSignaturesSimplex(TonlibModel):
    id: TonBlockIdExt
    signatures: list[BlockSignature]
    session_id: str
    slot: int
    candidate: str


class ShardBlockLink(TonlibModel):
    id: TonBlockIdExt
    proof: str


class BlockLinkBack(TonlibModel):
    to_key_block: bool
    from_block: TonBlockIdExt = Field(alias="from")
    to: TonBlockIdExt
    dest_proof: str
    proof: str
    state_proof: str


class ShardBlockProof(TonlibModel):
    from_block: TonBlockIdExt = Field(alias="from")
    mc_id: TonBlockIdExt
    links: list[ShardBlockLink]
    mc_proof: list[BlockLinkBack]


class Shards(TonlibModel):
    shards: list[TonBlockIdExt]


class BlockHeader(TonlibModel):
    id: TonBlockIdExt
    global_id: int
    version: int
    after_merge: bool
    after_split: bool
    before_split: bool
    want_merge: bool
    want_split: bool
    validator_list_hash_short: int
    catchain_seqno: int
    min_ref_mc_seqno: int
    is_key_block: bool
    prev_key_block_seqno: int
    start_lt: str
    end_lt: str
    gen_utime: int
    prev_blocks: list[TonBlockIdExt]


class OutMsgQueueSize(TonlibModel):
    id: TonBlockIdExt
    size: int


class OutMsgQueueSizes(TonlibModel):
    shards: list[OutMsgQueueSize]
    ext_msg_queue_size_limit: int


class MsgDataRaw(TonlibModel):
    type: Literal["msg.dataRaw"] = Field(default="msg.dataRaw", alias="@type")
    body: str | None = None
    init_state: str | None = None


class MsgDataText(TonlibModel):
    type: Literal["msg.dataText"] = Field(default="msg.dataText", alias="@type")
    text: str | None = None


class MsgDataDecryptedText(TonlibModel):
    type: Literal["msg.dataDecryptedText"] = Field(
        default="msg.dataDecryptedText",
        alias="@type",
    )
    text: str | None = None


class MsgDataEncryptedText(TonlibModel):
    type: Literal["msg.dataEncryptedText"] = Field(
        default="msg.dataEncryptedText",
        alias="@type",
    )
    text: str | None = None


MsgData = Annotated[
    MsgDataRaw | MsgDataText | MsgDataDecryptedText | MsgDataEncryptedText,
    Field(discriminator="type"),
]


class MessageStd(TonlibModel):
    hash: str
    source: AccountAddress
    destination: AccountAddress
    value: str
    extra_currencies: list[ExtraCurrencyBalance]
    fwd_fee: str
    ihr_fee: str
    created_lt: str
    body_hash: str
    msg_data: MsgData


class Message(TonlibModel):
    hash: str
    source: str
    destination: str
    value: str
    extra_currencies: list[ExtraCurrencyBalance]
    fwd_fee: str
    ihr_fee: str
    created_lt: str
    body_hash: str
    msg_data: MsgData
    message: str | None = None
    message_decode_error: str | None = None


class TransactionStd(TonlibModel):
    address: AccountAddress
    utime: int
    data: str
    transaction_id: InternalTransactionId
    fee: str
    storage_fee: str
    other_fee: str
    in_msg: MessageStd | None = None
    out_msgs: list[MessageStd]


class Transaction(TonlibModel):
    address: AccountAddress
    account: str
    utime: int
    data: str
    transaction_id: InternalTransactionId
    fee: str
    storage_fee: str
    other_fee: str
    in_msg: Message | None = None
    out_msgs: list[Message]


class TransactionExt(TonlibModel):
    address: AccountAddress
    account: str
    utime: int
    data: str
    transaction_id: InternalTransactionId
    fee: str
    storage_fee: str
    other_fee: str
    in_msg: MessageStd | None = None
    out_msgs: list[MessageStd]


class TransactionsStd(TonlibModel):
    transactions: list[TransactionStd]
    previous_transaction_id: InternalTransactionId


class ShortTxId(TonlibModel):
    mode: int
    account: str
    lt: str
    hash: str


class BlockTransactions(TonlibModel):
    id: TonBlockIdExt
    req_count: int
    incomplete: bool
    transactions: list[ShortTxId]


class BlockTransactionsExt(TonlibModel):
    id: TonBlockIdExt
    req_count: int
    incomplete: bool
    transactions: list[TransactionExt]


class TvmCell(TonlibModel):
    type: Literal["tvm.cell"] = Field(default="tvm.cell", alias="@type")
    bytes: str


class TvmSlice(TonlibModel):
    type: Literal["tvm.slice"] = Field(default="tvm.slice", alias="@type")
    bytes: str


class TvmNumberDecimal(TonlibModel):
    type: Literal["tvm.numberDecimal"] = Field(
        default="tvm.numberDecimal",
        alias="@type",
    )
    number: str


class TvmStackEntryNumber(TonlibModel):
    type: Literal["tvm.stackEntryNumber"] = Field(
        default="tvm.stackEntryNumber",
        alias="@type",
    )
    number: TvmNumberDecimal


class TvmStackEntryCell(TonlibModel):
    type: Literal["tvm.stackEntryCell"] = Field(
        default="tvm.stackEntryCell",
        alias="@type",
    )
    cell: TvmCell


class TvmStackEntrySlice(TonlibModel):
    type: Literal["tvm.stackEntrySlice"] = Field(
        default="tvm.stackEntrySlice",
        alias="@type",
    )
    slice: TvmSlice


class TvmStackEntryTuple(TonlibModel):
    type: Literal["tvm.stackEntryTuple"] = Field(
        default="tvm.stackEntryTuple",
        alias="@type",
    )
    tuple: TvmTuple


class TvmStackEntryList(TonlibModel):
    type: Literal["tvm.stackEntryList"] = Field(
        default="tvm.stackEntryList",
        alias="@type",
    )
    list: TvmList


class TvmStackEntryUnsupported(TonlibModel):
    type: Literal["tvm.stackEntryUnsupported"] = Field(
        default="tvm.stackEntryUnsupported",
        alias="@type",
    )


TvmStackEntry = Annotated[
    TvmStackEntryNumber
    | TvmStackEntryCell
    | TvmStackEntrySlice
    | TvmStackEntryTuple
    | TvmStackEntryList
    | TvmStackEntryUnsupported,
    Field(discriminator="type"),
]


class TvmTuple(TonlibModel):
    type: Literal["tvm.tuple"] = Field(default="tvm.tuple", alias="@type")
    elements: list[TvmStackEntry]


class TvmList(TonlibModel):
    type: Literal["tvm.list"] = Field(default="tvm.list", alias="@type")
    elements: list[TvmStackEntry]


class LegacyTvmCellData(ToncenterModel):
    b64: str
    len: int


class LegacyTvmCell(ToncenterModel):
    data: LegacyTvmCellData
    refs: list[LegacyTvmCell]
    special: bool


class LegacyStackEntryCell(ToncenterModel):
    bytes: str
    object: LegacyTvmCell | None = None


class RunGetMethodResult(TonlibModel):
    gas_used: int
    stack: list[list[t.Any]]
    exit_code: int
    block_id: TonBlockIdExt
    last_transaction_id: InternalTransactionId


class RunGetMethodStdResult(TonlibModel):
    gas_used: int
    stack: list[TvmStackEntry]
    exit_code: int


class LibraryEntry(TonlibModel):
    hash: str
    data: str


class LibraryResult(TonlibModel):
    result: list[LibraryEntry]


class TokenContent(ToncenterModel):
    type: str
    data: t.Any


class JettonMasterData(TonlibModel):
    type: Literal["ext.tokens.jettonMasterData"] = Field(
        default="ext.tokens.jettonMasterData",
        alias="@type",
    )
    address: str
    contract_type: Literal["jetton_master"] = "jetton_master"
    total_supply: str
    mintable: bool
    admin_address: str | None = None
    jetton_content: TokenContent
    jetton_wallet_code: str


class JettonWalletData(TonlibModel):
    type: Literal["ext.tokens.jettonWalletData"] = Field(
        default="ext.tokens.jettonWalletData",
        alias="@type",
    )
    address: str
    contract_type: Literal["jetton_wallet"] = "jetton_wallet"
    balance: str
    owner: str
    jetton: str
    mintless_is_claimed: bool | None = None
    jetton_wallet_code: str


class NftCollectionData(TonlibModel):
    type: Literal["ext.tokens.nftCollectionData"] = Field(
        default="ext.tokens.nftCollectionData",
        alias="@type",
    )
    address: str
    contract_type: Literal["nft_collection"] = "nft_collection"
    next_item_index: str
    owner_address: str | None = None
    collection_content: TokenContent


class NftItemData(TonlibModel):
    type: Literal["ext.tokens.nftItemData"] = Field(
        default="ext.tokens.nftItemData",
        alias="@type",
    )
    address: str
    contract_type: Literal["nft_item"] = "nft_item"
    init: bool
    index: str
    collection_address: str | None = None
    owner_address: str | None = None
    content: TokenContent | DnsContent


TokenData = Annotated[
    JettonMasterData | JettonWalletData | NftCollectionData | NftItemData,
    Field(discriminator="contract_type"),
]


class Fees(TonlibModel):
    in_fwd_fee: int
    storage_fee: int
    gas_fee: int
    fwd_fee: int


class QueryFees(TonlibModel):
    source_fees: Fees
    destination_fees: list[Fees]


class DetectAddressBase64Variant(TonlibModel):
    b64: str
    b64url: str


class DetectAddress(TonlibModel):
    raw_form: str
    bounceable: DetectAddressBase64Variant
    non_bounceable: DetectAddressBase64Variant
    given_type: str
    test_only: bool


class DetectHash(TonlibModel):
    b64: str
    b64url: str
    hex: str


class ResultOk(TonlibModel):
    type: Literal["ok"] = Field(default="ok", alias="@type")


class ExtMessageInfo(TonlibModel):
    hash: str
    hash_norm: str


class ConfigInfo(TonlibModel):
    config: TvmCell


class TonlibResponse(ToncenterModel):
    ok: bool = True
    result: t.Any = None
    extra: str | None = Field(default=None, alias="@extra")
    jsonrpc: str | None = None
    id: str | None = None


class TonlibErrorResponse(ToncenterModel):
    ok: bool = False
    error: str = ""
    code: int = 0
    extra: str | None = Field(default=None, alias="@extra")
    jsonrpc: str | None = None
    id: str | None = None


TvmStackEntryTuple.model_rebuild()
TvmStackEntryList.model_rebuild()
TvmTuple.model_rebuild()
TvmList.model_rebuild()
LegacyTvmCell.model_rebuild()


__all__ = [
    "AccountAddress",
    "AccountState",
    "AccountStateDns",
    "AccountStateEnum",
    "AccountStatePChan",
    "AccountStateRWallet",
    "AccountStateRaw",
    "AccountStateUninited",
    "AccountStateWalletHighloadV1",
    "AccountStateWalletHighloadV2",
    "AccountStateWalletV3",
    "AccountStateWalletV4",
    "AddressInformation",
    "BlockHeader",
    "BlockLinkBack",
    "BlockSignature",
    "BlockSignatures",
    "BlockSignaturesSimplex",
    "BlockTransactions",
    "BlockTransactionsExt",
    "ConfigInfo",
    "ConsensusBlock",
    "DetectAddress",
    "DetectAddressBase64Variant",
    "DetectHash",
    "DnsContent",
    "DnsRecord",
    "DnsRecordAdnlAddress",
    "DnsRecordNextResolver",
    "DnsRecordSet",
    "DnsRecordSmcAddress",
    "DnsRecordStorageAddress",
    "ExtMessageInfo",
    "ExtendedAddressInformation",
    "ExtraCurrencyBalance",
    "Fees",
    "InternalTransactionId",
    "JettonMasterData",
    "JettonWalletData",
    "LegacyStackEntryCell",
    "LegacyTvmCell",
    "LegacyTvmCellData",
    "LibraryEntry",
    "LibraryResult",
    "MasterchainInfo",
    "Message",
    "MessageStd",
    "MsgData",
    "MsgDataDecryptedText",
    "MsgDataEncryptedText",
    "MsgDataRaw",
    "MsgDataText",
    "NftCollectionData",
    "NftItemData",
    "OutMsgQueueSize",
    "OutMsgQueueSizes",
    "PChanConfig",
    "PChanState",
    "PChanStateClose",
    "PChanStateInit",
    "PChanStatePayout",
    "QueryFees",
    "RWalletConfig",
    "RWalletLimit",
    "ResultOk",
    "RunGetMethodResult",
    "RunGetMethodStdResult",
    "ShardBlockLink",
    "ShardBlockProof",
    "Shards",
    "ShortTxId",
    "SmcAddr",
    "TokenContent",
    "TokenData",
    "TonBlockIdExt",
    "ToncenterModel",
    "TonlibErrorResponse",
    "TonlibModel",
    "TonlibResponse",
    "Transaction",
    "TransactionExt",
    "TransactionStd",
    "TransactionsStd",
    "TvmCell",
    "TvmList",
    "TvmNumberDecimal",
    "TvmSlice",
    "TvmStackEntry",
    "TvmStackEntryCell",
    "TvmStackEntryList",
    "TvmStackEntryNumber",
    "TvmStackEntrySlice",
    "TvmStackEntryTuple",
    "TvmStackEntryUnsupported",
    "TvmTuple",
    "WalletInformation",
]
