from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Owner address — fetch all NFTs belonging to this account
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Fetch NFTs owned by the account
        # owner_address accepts list[str] — can query multiple owners at once
        # include_on_sale=True also returns NFTs listed on marketplaces
        result = await client.v3.nfts.get_nft_items(
            owner_address=[ACCOUNT],
            include_on_sale=True,
            limit=10,
        )

        for nft in result.nft_items or []:
            # address — NFT item contract address
            print(f"NFT: {nft.address}")

            # collection_address — the collection this NFT belongs to (None if standalone)
            print(f"Collection: {nft.collection_address}")

            # index — item index within the collection
            print(f"Index: {nft.index}")

            # content — on-chain or off-chain metadata (name, image, attributes, etc.)
            if nft.content:
                print(f"Content: {nft.content}")
            print()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
