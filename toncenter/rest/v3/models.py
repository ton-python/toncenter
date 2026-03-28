from __future__ import annotations

import typing as t
from enum import Enum

from pydantic import BaseModel, Field, RootModel


class FinalityState(str, Enum):
    """Finality level of a REST API response.

    Lifecycle: ``pending`` → ``confirmed`` → ``finalized``.
    Unknown values returned by the API are preserved as plain strings.
    """

    PENDING = "pending"
    CONFIRMED = "confirmed"
    FINALIZED = "finalized"


class AccountStateFull(BaseModel):
    account_state_hash: str | None = Field(default=None)
    address: str | None = Field(default=None)
    balance: str | None = Field(default=None)
    code_boc: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    contract_methods: list[int] | None = Field(default=None)
    data_boc: str | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    extra_currencies: dict[str, str] | None = Field(default=None)
    frozen_hash: str | None = Field(default=None)
    interfaces: list[str] | None = Field(default=None)
    last_transaction_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    status: str | None = Field(default=None)


class AddressBookRow(BaseModel):
    domain: str | None = Field(default=None)
    interfaces: list[str] | None = Field(default=None)
    user_friendly: str | None = Field(default=None)


class AddressBook(RootModel[dict[str, AddressBookRow]]):
    pass


class TokenInfo(BaseModel):
    description: str | None = Field(default=None)
    extra: dict[str, t.Any] | None = Field(default=None)
    image: str | None = Field(default=None)
    name: str | None = Field(default=None)
    nft_index: str | None = Field(default=None)
    symbol: str | None = Field(default=None)
    type: str | None = Field(default=None)
    valid: bool | None = Field(default=None)


class AddressMetadata(BaseModel):
    is_indexed: bool | None = Field(default=None)
    token_info: list[TokenInfo] | None = Field(default=None)


class Metadata(RootModel[dict[str, AddressMetadata]]):
    pass


class AccountStatesResponse(BaseModel):
    accounts: list[AccountStateFull] | None = Field(default=None)
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)


class WalletState(BaseModel):
    address: str | None = Field(default=None)
    balance: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    extra_currencies: dict[str, str] | None = Field(default=None)
    is_signature_allowed: bool | None = Field(default=None)
    is_wallet: bool | None = Field(default=None)
    last_transaction_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    seqno: int | None = Field(default=None)
    status: str | None = Field(default=None)
    wallet_id: int | None = Field(default=None)
    wallet_type: str | None = Field(default=None)


class WalletStatesResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)
    wallets: list[WalletState] | None = Field(default=None)


class AccountState(BaseModel):
    account_status: str | None = Field(default=None)
    balance: str | None = Field(default=None)
    code_boc: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    data_boc: str | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    extra_currencies: dict[str, str] | None = Field(default=None)
    frozen_hash: str | None = Field(default=None)
    hash: str | None = Field(default=None)


class MsgSize(BaseModel):
    bits: str | None = Field(default=None)
    cells: str | None = Field(default=None)


class ActionPhase(BaseModel):
    action_list_hash: str | None = Field(default=None)
    msgs_created: int | None = Field(default=None)
    no_funds: bool | None = Field(default=None)
    result_arg: int | None = Field(default=None)
    result_code: int | None = Field(default=None)
    skipped_actions: int | None = Field(default=None)
    spec_actions: int | None = Field(default=None)
    status_change: str | None = Field(default=None)
    success: bool | None = Field(default=None)
    tot_actions: int | None = Field(default=None)
    tot_msg_size: MsgSize | None = Field(default=None)
    total_action_fees: str | None = Field(default=None)
    total_fwd_fees: str | None = Field(default=None)
    valid: bool | None = Field(default=None)


class BlockId(BaseModel):
    seqno: int | None = Field(default=None)
    shard: str | None = Field(default=None)
    workchain: int | None = Field(default=None)


class Block(BaseModel):
    after_merge: bool | None = Field(default=None)
    after_split: bool | None = Field(default=None)
    before_split: bool | None = Field(default=None)
    created_by: str | None = Field(default=None)
    end_lt: str | None = Field(default=None)
    file_hash: str | None = Field(default=None)
    flags: int | None = Field(default=None)
    gen_catchain_seqno: int | None = Field(default=None)
    gen_utime: str | None = Field(default=None)
    global_id: int | None = Field(default=None)
    key_block: bool | None = Field(default=None)
    master_ref_seqno: int | None = Field(default=None)
    masterchain_block_ref: BlockId | None = Field(default=None)
    min_ref_mc_seqno: int | None = Field(default=None)
    prev_blocks: list[BlockId] | None = Field(default=None)
    prev_key_block_seqno: int | None = Field(default=None)
    rand_seed: str | None = Field(default=None)
    root_hash: str | None = Field(default=None)
    seqno: int | None = Field(default=None)
    shard: str | None = Field(default=None)
    start_lt: str | None = Field(default=None)
    tx_count: int | None = Field(default=None)
    validator_list_hash_short: int | None = Field(default=None)
    version: int | None = Field(default=None)
    vert_seqno: int | None = Field(default=None)
    vert_seqno_incr: bool | None = Field(default=None)
    want_merge: bool | None = Field(default=None)
    want_split: bool | None = Field(default=None)
    workchain: int | None = Field(default=None)


class BlocksResponse(BaseModel):
    blocks: list[Block] | None = Field(default=None)


class BouncePhase(BaseModel):
    fwd_fees: str | None = Field(default=None)
    msg_fees: str | None = Field(default=None)
    msg_size: MsgSize | None = Field(default=None)
    req_fwd_fees: str | None = Field(default=None)
    type: str | None = Field(default=None)


class ComputePhase(BaseModel):
    account_activated: bool | None = Field(default=None)
    exit_arg: int | None = Field(default=None)
    exit_code: int | None = Field(default=None)
    gas_credit: str | None = Field(default=None)
    gas_fees: str | None = Field(default=None)
    gas_limit: str | None = Field(default=None)
    gas_used: str | None = Field(default=None)
    mode: int | None = Field(default=None)
    msg_state_used: bool | None = Field(default=None)
    reason: str | None = Field(default=None)
    skipped: bool | None = Field(default=None)
    success: bool | None = Field(default=None)
    vm_final_state_hash: str | None = Field(default=None)
    vm_init_state_hash: str | None = Field(default=None)
    vm_steps: int | None = Field(default=None)


class CreditPhase(BaseModel):
    credit: str | None = Field(default=None)
    credit_extra_currencies: dict[str, str] | None = Field(default=None)
    due_fees_collected: str | None = Field(default=None)


class MasterchainInfo(BaseModel):
    first: Block | None = Field(default=None)
    last: Block | None = Field(default=None)


class MessageContent(BaseModel):
    body: str | None = Field(default=None)
    decoded: t.Any | None = Field(default=None)
    hash: str | None = Field(default=None)


class Message(BaseModel):
    bounce: bool | None = Field(default=None)
    bounced: bool | None = Field(default=None)
    created_at: str | None = Field(default=None)
    created_lt: str | None = Field(default=None)
    decoded_opcode: str | None = Field(default=None)
    destination: str | None = Field(default=None)
    extra_flags: str | None = Field(default=None)
    fwd_fee: str | None = Field(default=None)
    hash: str | None = Field(default=None)
    hash_norm: str | None = Field(default=None)
    ihr_disabled: bool | None = Field(default=None)
    ihr_fee: str | None = Field(default=None)
    import_fee: str | None = Field(default=None)
    in_msg_tx_hash: str | None = Field(default=None)
    init_state: MessageContent | None = Field(default=None)
    message_content: MessageContent | None = Field(default=None)
    opcode: str | None = Field(default=None)
    out_msg_tx_hash: str | None = Field(default=None)
    source: str | None = Field(default=None)
    value: str | None = Field(default=None)
    value_extra_currencies: dict[str, str] | None = Field(default=None)


class MessagesResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    messages: list[Message] | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)


class RequestError(BaseModel):
    code: int | None = Field(default=None)
    error: str | None = Field(default=None)


class SplitInfo(BaseModel):
    acc_split_depth: int | None = Field(default=None)
    cur_shard_pfx_len: int | None = Field(default=None)
    sibling_addr: str | None = Field(default=None)
    this_addr: str | None = Field(default=None)


class StoragePhase(BaseModel):
    status_change: str | None = Field(default=None)
    storage_fees_collected: str | None = Field(default=None)
    storage_fees_due: str | None = Field(default=None)


class TransactionDescr(BaseModel):
    aborted: bool | None = Field(default=None)
    action: ActionPhase | None = Field(default=None)
    bounce: BouncePhase | None = Field(default=None)
    compute_ph: ComputePhase | None = Field(default=None)
    credit_first: bool | None = Field(default=None)
    credit_ph: CreditPhase | None = Field(default=None)
    destroyed: bool | None = Field(default=None)
    installed: bool | None = Field(default=None)
    is_tock: bool | None = Field(default=None)
    split_info: SplitInfo | None = Field(default=None)
    storage_ph: StoragePhase | None = Field(default=None)
    type: str | None = Field(default=None)


class Transaction(BaseModel):
    account: str | None = Field(default=None)
    account_state_after: AccountState | None = Field(default=None)
    account_state_before: AccountState | None = Field(default=None)
    block_ref: BlockId | None = Field(default=None)
    description: TransactionDescr | None = Field(default=None)
    emulated: bool | None = Field(default=None)
    end_status: str | None = Field(default=None)
    finality: FinalityState | str | None = Field(default=None)
    hash: str | None = Field(default=None)
    in_msg: Message | None = Field(default=None)
    lt: str | None = Field(default=None)
    mc_block_seqno: int | None = Field(default=None)
    now: int | None = Field(default=None)
    orig_status: str | None = Field(default=None)
    out_msgs: list[Message] | None = Field(default=None)
    prev_trans_hash: str | None = Field(default=None)
    prev_trans_lt: str | None = Field(default=None)
    total_fees: str | None = Field(default=None)
    total_fees_extra_currencies: dict[str, str] | None = Field(default=None)
    trace_external_hash: str | None = Field(default=None)
    trace_id: str | None = Field(default=None)


class TransactionsResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    transactions: list[Transaction] | None = Field(default=None)


class Action(BaseModel):
    accounts: list[str] | None = Field(default=None)
    action_id: str | None = Field(default=None)
    details: t.Any | None = Field(default=None)
    end_lt: str | None = Field(default=None)
    end_utime: int | None = Field(default=None)
    finality: FinalityState | str | None = Field(default=None)
    start_lt: str | None = Field(default=None)
    start_utime: int | None = Field(default=None)
    success: bool | None = Field(default=None)
    trace_end_lt: str | None = Field(default=None)
    trace_end_utime: int | None = Field(default=None)
    trace_external_hash: str | None = Field(default=None)
    trace_external_hash_norm: str | None = Field(default=None)
    trace_id: str | None = Field(default=None)
    trace_mc_seqno_end: int | None = Field(default=None)
    transactions: list[str] | None = Field(default=None)
    transactions_full: list[Transaction] | None = Field(default=None)
    type: str | None = Field(default=None)


class ActionsResponse(BaseModel):
    actions: list[Action] | None = Field(default=None)
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)


class TraceMeta(BaseModel):
    classification_state: str | None = Field(default=None)
    messages: int | None = Field(default=None)
    pending_messages: int | None = Field(default=None)
    trace_state: str | None = Field(default=None)
    transactions: int | None = Field(default=None)


class TraceNode(BaseModel):
    children: list[TraceNode] | None = Field(default=None)
    in_msg: Message | None = Field(default=None)
    in_msg_hash: str | None = Field(default=None)
    transaction: Transaction | None = Field(default=None)
    tx_hash: str | None = Field(default=None)


class Trace(BaseModel):
    actions: list[Action] | None = Field(default=None)
    end_lt: str | None = Field(default=None)
    end_utime: int | None = Field(default=None)
    external_hash: str | None = Field(default=None)
    is_incomplete: bool | None = Field(default=None)
    mc_seqno_end: str | None = Field(default=None)
    mc_seqno_start: str | None = Field(default=None)
    start_lt: str | None = Field(default=None)
    start_utime: int | None = Field(default=None)
    trace: TraceNode | None = Field(default=None)
    trace_id: str | None = Field(default=None)
    trace_info: TraceMeta | None = Field(default=None)
    transactions: dict[str, Transaction] | None = Field(default=None)
    transactions_order: list[str] | None = Field(default=None)
    warning: str | None = Field(default=None)


class TracesResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)
    traces: list[Trace] | None = Field(default=None)


class V2AddressInformation(BaseModel):
    balance: str | None = Field(default=None)
    code: str | None = Field(default=None)
    data: str | None = Field(default=None)
    frozen_hash: str | None = Field(default=None)
    last_transaction_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    status: str | None = Field(default=None)


class V2EstimateFeeRequest(BaseModel):
    address: str | None = Field(default=None)
    body: str | None = Field(default=None)
    ignore_chksig: bool | None = Field(default=None)
    init_code: str | None = Field(default=None)
    init_data: str | None = Field(default=None)


class V2EstimatedFee(BaseModel):
    fwd_fee: int | None = Field(default=None)
    gas_fee: int | None = Field(default=None)
    in_fwd_fee: int | None = Field(default=None)
    storage_fee: int | None = Field(default=None)


class V2EstimateFeeResult(BaseModel):
    destination_fees: list[V2EstimatedFee] | None = Field(default=None)
    source_fees: V2EstimatedFee | None = Field(default=None)


class V2StackEntity(BaseModel):
    type: str | None = Field(default=None)
    value: t.Any | None = Field(default=None)


class V2RunGetMethodRequest(BaseModel):
    address: str | None = Field(default=None)
    method: str | None = Field(default=None)
    stack: list[V2StackEntity] | None = Field(default=None)


class V2RunGetMethodResult(BaseModel):
    gas_used: int | None = Field(default=None)
    exit_code: int | None = Field(default=None)
    stack: list[V2StackEntity] | None = Field(default=None)


class V2SendMessageRequest(BaseModel):
    boc: str | None = Field(default=None)


class V2SendMessageResult(BaseModel):
    message_hash: str | None = Field(default=None)
    message_hash_norm: str | None = Field(default=None)


class V2WalletInformation(BaseModel):
    balance: str | None = Field(default=None)
    last_transaction_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    seqno: int | None = Field(default=None)
    status: str | None = Field(default=None)
    wallet_id: int | None = Field(default=None)
    wallet_type: str | None = Field(default=None)


class DNSRecord(BaseModel):
    dns_next_resolver: str | None = Field(default=None)
    dns_site_adnl: str | None = Field(default=None)
    dns_storage_bag_id: str | None = Field(default=None)
    dns_wallet: str | None = Field(default=None)
    domain: str | None = Field(default=None)
    nft_item_address: str | None = Field(default=None)
    nft_item_owner: str | None = Field(default=None)


class DNSRecordsResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    records: list[DNSRecord] | None = Field(default=None)


class JettonBurn(BaseModel):
    amount: str | None = Field(default=None)
    custom_payload: str | None = Field(default=None)
    decoded_custom_payload: t.Any | None = Field(default=None)
    jetton_master: str | None = Field(default=None)
    jetton_wallet: str | None = Field(default=None)
    owner: str | None = Field(default=None)
    query_id: str | None = Field(default=None)
    response_destination: str | None = Field(default=None)
    trace_id: str | None = Field(default=None)
    transaction_aborted: bool | None = Field(default=None)
    transaction_hash: str | None = Field(default=None)
    transaction_lt: str | None = Field(default=None)
    transaction_now: int | None = Field(default=None)


class JettonBurnsResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    jetton_burns: list[JettonBurn] | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)


class JettonMaster(BaseModel):
    address: str | None = Field(default=None)
    admin_address: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    jetton_content: dict[str, t.Any] | None = Field(default=None)
    jetton_wallet_code_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    mintable: bool | None = Field(default=None)
    total_supply: str | None = Field(default=None)


class JettonMastersResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    jetton_masters: list[JettonMaster] | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)


class JettonTransfer(BaseModel):
    amount: str | None = Field(default=None)
    custom_payload: str | None = Field(default=None)
    decoded_custom_payload: t.Any | None = Field(default=None)
    decoded_forward_payload: t.Any | None = Field(default=None)
    destination: str | None = Field(default=None)
    forward_payload: str | None = Field(default=None)
    forward_ton_amount: str | None = Field(default=None)
    jetton_master: str | None = Field(default=None)
    query_id: str | None = Field(default=None)
    response_destination: str | None = Field(default=None)
    source: str | None = Field(default=None)
    source_wallet: str | None = Field(default=None)
    trace_id: str | None = Field(default=None)
    transaction_aborted: bool | None = Field(default=None)
    transaction_hash: str | None = Field(default=None)
    transaction_lt: str | None = Field(default=None)
    transaction_now: int | None = Field(default=None)


class JettonTransfersResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    jetton_transfers: list[JettonTransfer] | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)


class JettonWalletMintlessInfo(BaseModel):
    amount: str | None = Field(default=None)
    custom_payload_api_uri: list[str] | None = Field(default=None)
    expire_at: int | None = Field(default=None)
    start_from: int | None = Field(default=None)


class JettonWallet(BaseModel):
    address: str | None = Field(default=None)
    balance: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    jetton: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    mintless_info: JettonWalletMintlessInfo | None = Field(default=None)
    owner: str | None = Field(default=None)


class JettonWalletsResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    jetton_wallets: list[JettonWallet] | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)


class IndexOrderAction(BaseModel):
    body_raw: list[int] | None = Field(default=None)
    destination: str | None = Field(default=None)
    error: str | None = Field(default=None)
    parsed: bool | None = Field(default=None)
    parsed_body: t.Any | None = Field(default=None)
    parsed_body_type: str | None = Field(default=None)
    send_mode: int | None = Field(default=None)
    value: str | None = Field(default=None)


class MultisigOrder(BaseModel):
    actions: list[IndexOrderAction] | None = Field(default=None)
    address: str | None = Field(default=None)
    approvals_mask: str | None = Field(default=None)
    approvals_num: int | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    expiration_date: int | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    multisig_address: str | None = Field(default=None)
    order_boc: str | None = Field(default=None)
    order_seqno: str | None = Field(default=None)
    sent_for_execution: bool | None = Field(default=None)
    signers: list[str] | None = Field(default=None)
    threshold: int | None = Field(default=None)


class Multisig(BaseModel):
    address: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    next_order_seqno: str | None = Field(default=None)
    orders: list[MultisigOrder] | None = Field(default=None)
    proposers: list[str] | None = Field(default=None)
    signers: list[str] | None = Field(default=None)
    threshold: int | None = Field(default=None)


class MultisigOrderResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    orders: list[MultisigOrder] | None = Field(default=None)


class MultisigResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    multisigs: list[Multisig] | None = Field(default=None)


class NFTCollection(BaseModel):
    address: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    collection_content: dict[str, t.Any] | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    next_item_index: str | None = Field(default=None)
    owner_address: str | None = Field(default=None)


class NFTCollectionsResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)
    nft_collections: list[NFTCollection] | None = Field(default=None)


class NFTItem(BaseModel):
    address: str | None = Field(default=None)
    auction_contract_address: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    collection: NFTCollection | None = Field(default=None)
    collection_address: str | None = Field(default=None)
    content: dict[str, t.Any] | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    index: str | None = Field(default=None)
    init: bool | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    on_sale: bool | None = Field(default=None)
    owner_address: str | None = Field(default=None)
    real_owner: str | None = Field(default=None)
    sale_contract_address: str | None = Field(default=None)


class NFTItemsResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)
    nft_items: list[NFTItem] | None = Field(default=None)


class NFTSale(BaseModel):
    address: str | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    created_at: int | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    details: t.Any | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    marketplace_address: str | None = Field(default=None)
    nft_address: str | None = Field(default=None)
    nft_item: NFTItem | None = Field(default=None)
    nft_owner_address: str | None = Field(default=None)
    type: str | None = Field(default=None)


class NFTSalesResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)
    nft_sales: list[NFTSale] | None = Field(default=None)


class NFTTransfer(BaseModel):
    custom_payload: str | None = Field(default=None)
    decoded_custom_payload: t.Any | None = Field(default=None)
    decoded_forward_payload: t.Any | None = Field(default=None)
    forward_amount: str | None = Field(default=None)
    forward_payload: str | None = Field(default=None)
    new_owner: str | None = Field(default=None)
    nft_address: str | None = Field(default=None)
    nft_collection: str | None = Field(default=None)
    old_owner: str | None = Field(default=None)
    query_id: str | None = Field(default=None)
    response_destination: str | None = Field(default=None)
    trace_id: str | None = Field(default=None)
    transaction_aborted: bool | None = Field(default=None)
    transaction_hash: str | None = Field(default=None)
    transaction_lt: str | None = Field(default=None)
    transaction_now: int | None = Field(default=None)


class NFTTransfersResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    metadata: Metadata | None = Field(default=None)
    nft_transfers: list[NFTTransfer] | None = Field(default=None)


class AccountBalance(BaseModel):
    account: str | None = Field(default=None)
    balance: str | None = Field(default=None)


class DecodeRequest(BaseModel):
    bodies: list[str] | None = Field(default=None)
    opcodes: list[str] | None = Field(default=None)


class DecodeResponse(BaseModel):
    bodies: list[dict[str, t.Any]] | None = Field(default=None)
    opcodes: list[str] | None = Field(default=None)


class IndexVestingInfo(BaseModel):
    address: str | None = Field(default=None)
    cliff_duration: int | None = Field(default=None)
    owner_address: str | None = Field(default=None)
    sender_address: str | None = Field(default=None)
    start_time: int | None = Field(default=None)
    total_amount: str | None = Field(default=None)
    total_duration: int | None = Field(default=None)
    unlock_period: int | None = Field(default=None)
    whitelist: list[str] | None = Field(default=None)


class VestingContractsResponse(BaseModel):
    address_book: AddressBook | None = Field(default=None)
    vesting_contracts: list[IndexVestingInfo] | None = Field(default=None)


TraceNode.model_rebuild()

__all__ = [
    "AccountBalance",
    "AccountState",
    "AccountStateFull",
    "AccountStatesResponse",
    "Action",
    "ActionPhase",
    "ActionsResponse",
    "AddressBook",
    "AddressBookRow",
    "AddressMetadata",
    "Block",
    "BlockId",
    "BlocksResponse",
    "BouncePhase",
    "ComputePhase",
    "CreditPhase",
    "DNSRecord",
    "DNSRecordsResponse",
    "DecodeRequest",
    "DecodeResponse",
    "FinalityState",
    "IndexOrderAction",
    "IndexVestingInfo",
    "JettonBurn",
    "JettonBurnsResponse",
    "JettonMaster",
    "JettonMastersResponse",
    "JettonTransfer",
    "JettonTransfersResponse",
    "JettonWallet",
    "JettonWalletMintlessInfo",
    "JettonWalletsResponse",
    "MasterchainInfo",
    "Message",
    "MessageContent",
    "MessagesResponse",
    "Metadata",
    "MsgSize",
    "Multisig",
    "MultisigOrder",
    "MultisigOrderResponse",
    "MultisigResponse",
    "NFTCollection",
    "NFTCollectionsResponse",
    "NFTItem",
    "NFTItemsResponse",
    "NFTSale",
    "NFTSalesResponse",
    "NFTTransfer",
    "NFTTransfersResponse",
    "RequestError",
    "SplitInfo",
    "StoragePhase",
    "TokenInfo",
    "Trace",
    "TraceMeta",
    "TraceNode",
    "TracesResponse",
    "Transaction",
    "TransactionDescr",
    "TransactionsResponse",
    "V2AddressInformation",
    "V2EstimateFeeRequest",
    "V2EstimateFeeResult",
    "V2EstimatedFee",
    "V2RunGetMethodRequest",
    "V2RunGetMethodResult",
    "V2SendMessageRequest",
    "V2SendMessageResult",
    "V2StackEntity",
    "V2WalletInformation",
    "VestingContractsResponse",
    "WalletState",
    "WalletStatesResponse",
]
