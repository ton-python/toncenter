from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address — fetch parsed actions for this account
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch recent actions for the account
        # Actions are high-level interpretations of transactions
        # (ton_transfer, jetton_transfer, nft_mint, subscribe, etc.)
        result = await client.v3.actions.get_actions(account=ACCOUNT, limit=5)

        for action in result.actions or []:
            # type — action kind (ton_transfer, jetton_transfer, nft_mint, etc.)
            print(f"Action: {action.type}")

            # trace_external_hash — groups related actions into a single trace
            print(f"Trace: {action.trace_external_hash}")

            # finality — finalization state (finalized, unknown_3, etc.)
            print(f"Finality: {action.finality}")
            print()

        # Filter by specific action types
        # action_type accepts list[str] — only return matching types
        jetton_actions = await client.v3.actions.get_actions(
            account=ACCOUNT,
            action_type=["jetton_transfer"],
            limit=5,
        )
        print(f"Jetton transfers: {len(jetton_actions.actions or [])}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
