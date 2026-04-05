import asyncio

from toncenter.streaming.models import (
    AccountStateNotification,
    ActionsNotification,
    Finality,
    JettonsNotification,
    TransactionsNotification,
)
from toncenter.streaming.ws import ToncenterWebSocket
from toncenter.types import Network

# TON Center API key — get one via @toncenter bot on Telegram
API_KEY = "YOUR_API_KEY"

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account addresses to track — any form (raw, bounceable, non-bounceable)
ACCOUNT = "UQBAjaOyi2wGWlk-EDkSabqqnF-MrrwMadnwqrurKpkla4QB"
ANOTHER_ACCOUNT = "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"


async def main() -> None:
    client = ToncenterWebSocket(API_KEY, NETWORK)

    # Register handlers — same decorator API as SSE
    # WebSocket additionally supports dynamic subscription changes (see below)

    @client.on_transactions(min_finality=Finality.FINALIZED)
    async def handle_transactions(event: TransactionsNotification) -> None:
        for tx in event.transactions:
            print(f"TX: {tx.get('hash', '?')} | finality={event.finality}")

    @client.on_actions(min_finality=Finality.CONFIRMED)
    async def handle_actions(event: ActionsNotification) -> None:
        for action in event.actions:
            print(f"Action: {action.get('type', '?')} | finality={event.finality}")

    @client.on_account_states(min_finality=Finality.FINALIZED)
    async def handle_account_state(event: AccountStateNotification) -> None:
        balance = event.state.balance if event.state else "?"
        print(f"Account state: {event.account} | balance={balance}")

    @client.on_jettons(min_finality=Finality.FINALIZED)
    async def handle_jettons(event: JettonsNotification) -> None:
        if event.jetton:
            print(f"Jetton: {event.jetton.jetton} | balance={event.jetton.balance}")

    # Dynamic subscription change — WebSocket exclusive feature
    # After start() establishes the connection, you can change what you're subscribed to
    # without reconnecting. SSE does not support this.
    async def change_subscription_later() -> None:
        # Wait until connected
        await client.wait_subscribed(timeout=30)
        print("Connected! Waiting 15s before changing subscription...")
        await asyncio.sleep(15)

        # Replace current subscription with a new one (snapshot semantics)
        # This replaces ALL addresses and filters — not incremental
        print("Switching subscription to another account...")
        await client.dynamic_subscribe(
            addresses=[ANOTHER_ACCOUNT],
            types=["transactions", "actions"],
            min_finality=Finality.FINALIZED,
        )
        print("Subscription updated.")

        await asyncio.sleep(30)
        await client.stop()

    # Run dynamic subscription change in background
    background_tasks: set[asyncio.Task[None]] = set()
    task = asyncio.create_task(change_subscription_later())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    print("Subscribing via WebSocket...")
    await client.start(
        addresses=[ACCOUNT],
        include_address_book=True,
    )
    print("Stopped.")


if __name__ == "__main__":
    asyncio.run(main())
