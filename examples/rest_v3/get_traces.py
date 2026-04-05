from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address — fetch execution traces for this account
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch traces — full execution trees of multi-step transactions
        # A trace groups all transactions triggered by a single external message
        result = await client.v3.actions.get_traces(
            account=ACCOUNT,
            limit=3,
        )

        for trace in result.traces or []:
            # trace_id — unique trace identifier
            print(f"Trace: {trace.trace_id}")

            # external_hash — hash of the external message that started the trace
            print(f"External hash: {trace.external_hash}")

            # mc_seqno_start / mc_seqno_end — masterchain block range (strings)
            print(f"MC seqno: {trace.mc_seqno_start} -> {trace.mc_seqno_end}")

            # transactions — dict mapping tx_hash -> Transaction
            if trace.transactions:
                print(f"Transactions: {len(trace.transactions)}")
                for tx_hash in trace.transactions:
                    print(f"  TX: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
