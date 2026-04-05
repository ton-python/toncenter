from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address — fetch indexed transactions for this account
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch recent transactions (V3 indexed data — richer than V2)
        # account accepts list[str] — can query multiple accounts at once
        # sort: "desc" (newest first) or "asc" (oldest first)
        result = await client.v3.blockchain.get_transactions(
            account=[ACCOUNT],
            limit=5,
            sort="desc",
        )

        for tx in result.transactions or []:
            # hash — transaction hash (hex)
            print(f"Hash: {tx.hash}")

            # lt — logical time (monotonically increasing per account)
            print(f"LT: {tx.lt}")

            # account — which account this transaction belongs to
            print(f"Account: {tx.account}")

            # now — block generation Unix timestamp
            print(f"Time: {tx.now}")

            # total_fees — total fees charged for this transaction
            print(f"Fees: {tx.total_fees}")
            print()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
