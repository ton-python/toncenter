from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network
from toncenter.utils import to_amount

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Accounts to inspect — V3 supports batch queries (up to 1000 addresses)
ACCOUNTS = [
    "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0",
    "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
]


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch account states in batch — more efficient than querying one by one
        # include_boc=True (default) includes code and data BOCs
        result = await client.v3.accounts.get_account_states(ACCOUNTS)

        for state in result.accounts or []:
            # address — account address
            print(f"Address: {state.address}")

            # balance — in nanotons
            if state.balance is not None:
                print(f"Balance: {to_amount(int(state.balance))} TON")

            # status — account status (active, uninit, frozen, nonexist)
            print(f"Status: {state.status}")

            # code_hash / data_hash — contract identification
            print(f"Code hash: {state.code_hash}")
            print()

        # Get wallet-specific information (seqno, wallet type, etc.)
        wallets = await client.v3.accounts.get_wallet_states(ACCOUNTS)
        for w in wallets.wallets or []:
            print(f"Wallet: {w.address} | seqno={w.seqno} | type={w.wallet_type}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
