from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network
from toncenter.utils import to_amount

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Destination address — in any form (raw, bounceable, non-bounceable)
ADDRESS = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"

# Base64-encoded message body BoC
# This is the body cell of the message (not the full external message)
BODY = "te6cckEBAQEAAgAAAEysuc0="


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Estimate fees for sending a message before broadcasting
        # ignore_chksig=True (default) — skip signature verification during estimation
        # init_code / init_data — provide for contract deployment messages
        fees = await client.v2.send.estimate_fee(ADDRESS, BODY)

        # source_fees — fees charged on the sender side
        src = fees.source_fees
        print(f"In fwd fee:  {to_amount(src.in_fwd_fee)} TON")
        print(f"Storage fee: {to_amount(src.storage_fee)} TON")
        print(f"Gas fee:     {to_amount(src.gas_fee)} TON")
        print(f"Fwd fee:     {to_amount(src.fwd_fee)} TON")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
