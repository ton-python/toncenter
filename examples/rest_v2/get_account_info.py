from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network
from toncenter.utils import to_amount

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address to inspect — any format works (raw, bounceable, non-bounceable)
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch account information
        # Returns: balance, status, frozen hash, last transaction
        info = await client.v2.accounts.get_address_information(ACCOUNT)

        # balance is in nanotons (1 TON = 10^9 nanotons)
        # to_amount() converts nanotons to human-readable Decimal
        print(f"Balance: {to_amount(int(info.balance))} TON")

        # state — active, uninitialized, or frozen
        print(f"Status: {info.state}")

        # frozen_hash — non-empty when account is frozen
        print(f"Frozen hash: {info.frozen_hash}")

        # last_transaction_id — logical time and hash of the latest transaction
        print(f"Last TX: lt={info.last_transaction_id.lt} | hash={info.last_transaction_id.hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
