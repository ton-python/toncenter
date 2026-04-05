from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Address in any format — will be converted to all known formats
ACCOUNT = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Detect and convert an address to all known formats
        # Accepts raw, bounceable, or non-bounceable address
        detected = await client.v2.utils.detect_address(ACCOUNT)

        # raw_form — workchain:hex_hash (e.g., 0:14c584a8f94c28...)
        print(f"Raw: {detected.raw_form}")

        # bounceable — for smart contracts (base64 and base64url variants)
        print(f"Bounceable (b64): {detected.bounceable.b64}")
        print(f"Bounceable (url-safe): {detected.bounceable.b64url}")

        # non_bounceable — for wallets receiving TON (base64 and base64url variants)
        print(f"Non-bounceable (b64): {detected.non_bounceable.b64}")
        print(f"Non-bounceable (url-safe): {detected.non_bounceable.b64url}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
