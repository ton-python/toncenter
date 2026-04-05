from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Serialized signed message in base64 (BOC — Bag of Cells)
# Any library that can build and sign TON messages will produce a BOC
# Recommended: tonutils (pip install tonutils) — wallets, jetton transfers, NFT ops, etc.
BOC = "te6cckEBAQEAAgAAAEysuc0="


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Send the signed message to the blockchain
        # The BOC must be fully signed — TON Center broadcasts it as-is
        # Raises ToncenterClientError if the message is rejected
        # Returns ResultOk on success (no extra data)
        await client.v2.send.send_boc(BOC)
        print("Message accepted by the network")

        # send_boc_return_hash() does the same but also returns the message hash
        # Useful for tracking the message after submission
        ext_msg = await client.v2.send.send_boc_return_hash(BOC)
        print(f"Message hash: {ext_msg.hash}")
        print(f"Normalized hash: {ext_msg.hash_norm}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
