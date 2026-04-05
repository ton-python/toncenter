import asyncio

from toncenter.streaming.models import (
    AccountStateNotification,
    ActionsNotification,
    Finality,
    JettonsNotification,
    TransactionsNotification,
)
from toncenter.streaming.sse import ToncenterSSE
from toncenter.types import Network

# TON Center API key — get one via @toncenter bot on Telegram
API_KEY = "YOUR_API_KEY"

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address to track — any form (raw, bounceable, non-bounceable)
ACCOUNT = "UQBAjaOyi2wGWlk-EDkSabqqnF-MrrwMadnwqrurKpkla4QB"


async def main() -> None:
    client = ToncenterSSE(API_KEY, NETWORK)

    # Register handlers via decorators before calling start()
    # Each decorator subscribes to a specific notification type
    # min_finality controls when handlers fire:
    #   PENDING    — as soon as the transaction is seen (unconfirmed)
    #   CONFIRMED  — included in a block but not yet finalized
    #   FINALIZED  — irreversible (default)

    @client.on_transactions(min_finality=Finality.FINALIZED)
    async def handle_transactions(event: TransactionsNotification) -> None:
        # event.transactions — list of raw transaction dicts
        # event.trace_external_hash_norm — trace hash grouping related TXs
        # event.is_finalized / is_confirmed / is_pending — finality helpers
        for tx in event.transactions:
            print(f"TX: {tx.get('hash', '?')} | finality={event.finality}")

    @client.on_actions(min_finality=Finality.CONFIRMED)
    async def handle_actions(event: ActionsNotification) -> None:
        # event.actions — list of parsed action dicts (ton_transfer, jetton_transfer, etc.)
        # Use action_types= in the decorator to filter by specific action types
        for action in event.actions:
            print(f"Action: {action.get('type', '?')} | finality={event.finality}")

    @client.on_account_states(min_finality=Finality.FINALIZED)
    async def handle_account_state(event: AccountStateNotification) -> None:
        # event.account — address that changed
        # event.state — AccountState with hash, balance, account_status, etc.
        # Note: account_state_change does not support PENDING finality
        balance = event.state.balance if event.state else "?"
        print(f"Account state: {event.account} | balance={balance}")

    @client.on_jettons(min_finality=Finality.FINALIZED)
    async def handle_jettons(event: JettonsNotification) -> None:
        # event.jetton — JettonWallet with address, balance, owner, jetton master
        # Note: jettons_change does not support PENDING finality
        if event.jetton:
            print(f"Jetton: {event.jetton.jetton} | balance={event.jetton.balance}")

    # start() creates a session, subscribes, and blocks until stop() is called
    # addresses — which accounts to monitor (required for all types except trace)
    # include_address_book — resolve addresses to DNS names in notifications
    # include_metadata — include token metadata in notifications

    # Auto-stop after 60 seconds for demo purposes
    async def _stop_later() -> None:
        await asyncio.sleep(60)
        await client.stop()

    background_tasks: set[asyncio.Task[None]] = set()
    task = asyncio.create_task(_stop_later())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    print("Subscribing via SSE...")
    await client.start(
        addresses=[ACCOUNT],
        include_address_book=True,
    )
    print("Stopped.")


if __name__ == "__main__":
    asyncio.run(main())
