from toncenter.rest.client import ToncenterRestClient
from toncenter.types import Network

# TON Center API key — optional for REST (~1 RPS without key)
# Get one via @toncenter bot on Telegram for higher limits
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# .ton domain to resolve — currently .ton and .t.me DNS are supported
DOMAIN = "foundation.ton"


async def main() -> None:
    async with ToncenterRestClient(API_KEY, NETWORK) as client:
        # Resolve a .ton DNS name to its linked wallet address
        # Returns DNS records — dns_wallet contains the wallet address
        result = await client.v3.dns.get_dns_records(domain=DOMAIN)

        for record in result.records or []:
            # domain — the resolved domain name
            print(f"Domain: {record.domain}")

            # dns_wallet — wallet address linked to this domain (if set)
            if record.dns_wallet:
                print(f"Wallet: {record.dns_wallet}")

            # dns_next_resolver — points to a sub-resolver for nested domains
            if record.dns_next_resolver:
                print(f"Next resolver: {record.dns_next_resolver}")
            print()

        # Reverse lookup — find domains owned by a wallet address
        wallet = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"
        reverse = await client.v3.dns.get_dns_records(wallet=wallet)
        for record in reverse.records or []:
            print(f"{wallet} owns: {record.domain}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
