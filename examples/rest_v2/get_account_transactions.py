from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address to fetch transactions for
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch recent transactions for the account
        # limit: maximum number of transactions to return
        # Returns: list of transactions with messages, fees, and metadata
        txs = await client.v2.transactions.get_transactions(ACCOUNT, limit=5)

        for tx in txs:
            # transaction_id — unique identifier (logical time + hash)
            print(f"TX: lt={tx.transaction_id.lt} | hash={tx.transaction_id.hash}")

            # fee — total transaction fee in nanotons
            print(f"Fee: {tx.fee}")

            # in_msg — incoming message that triggered this transaction
            # out_msgs — outgoing messages produced by this transaction
            if tx.in_msg:
                print(f"In: {tx.in_msg.source} -> {tx.in_msg.destination}")
            print(f"Out messages: {len(tx.out_msgs)}")
            print()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
