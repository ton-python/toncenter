from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address — fetch jetton transfer history for this owner
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch recent jetton transfers for the account
        # direction: "in" (received), "out" (sent), or None (both)
        # sort: "desc" (newest first) or "asc" (oldest first)
        result = await client.v3.jettons.get_jetton_transfers(
            owner_address=[ACCOUNT],
            limit=5,
            sort="desc",
        )

        for transfer in result.jetton_transfers or []:
            # source / destination — sender and receiver wallet addresses
            print(f"From: {transfer.source}")
            print(f"To: {transfer.destination}")

            # amount — transfer amount in base units
            print(f"Amount: {transfer.amount}")

            # jetton_master — which token was transferred
            print(f"Jetton: {transfer.jetton_master}")

            # transaction_hash — hash of the underlying transaction
            print(f"TX: {transfer.transaction_hash}")
            print()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
