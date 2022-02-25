from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coin, Coins


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.market.swap_rate(Coin.parse("10000uluna"), "uusd")
    print(result)
    result = terra.market.terra_pool_delta()
    print(result)
    result = terra.market.parameters()
    print(result)


main()
