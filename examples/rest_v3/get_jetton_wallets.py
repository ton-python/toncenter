from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address — fetch all jetton balances for this owner
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch jetton wallets owned by the account
        # owner_address accepts list[str] — can query multiple owners at once
        # exclude_zero_balance=True filters out empty wallets
        result = await client.v3.jettons.get_jetton_wallets(
            owner_address=[ACCOUNT],
            exclude_zero_balance=True,
            limit=10,
        )

        for jw in result.jetton_wallets or []:
            # jetton — master contract address (identifies the token type)
            print(f"Jetton master: {jw.jetton}")

            # balance — token balance in base units (smallest denomination)
            print(f"Balance: {jw.balance}")

            # address — this specific jetton wallet contract address
            print(f"Wallet: {jw.address}")
            print()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
