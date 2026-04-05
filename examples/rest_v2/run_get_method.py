from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Wallet address — seqno is a standard get-method on all wallet contracts
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Run a read-only get-method on a smart contract
        # method: method name (string) or numeric ID
        # stack: input parameters in legacy 2-tuple format (empty for seqno)
        result = await client.v2.runmethod.run_get_method(ACCOUNT, "seqno")

        # exit_code — 0 means success, non-zero indicates an error
        print(f"Exit code: {result.exit_code}")

        # stack — return values from the method in 2-tuple format
        # For seqno: [["num", "0x..."]] — one integer on the stack
        print(f"Stack: {result.stack}")

        # run_get_method_std() returns the same data but with typed TVM stack format
        # Useful when you need structured parsing of complex return values
        result_std = await client.v2.runmethod.run_get_method_std(ACCOUNT, "seqno")
        print(f"Typed stack: {result_std.stack}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
