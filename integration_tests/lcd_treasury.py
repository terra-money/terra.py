from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.treasury.tax_cap("uusd")
    print(result)
    result = terra.treasury.tax_rate()
    print(result)
    result = terra.treasury.tax_rate(6248404)
    print(result)
    result = terra.treasury.reward_weight()
    print(result)
    result = terra.treasury.tax_proceeds()
    print(result)
    result = terra.treasury.seigniorage_proceeds()
    print(result)
    result = terra.treasury.parameters()
    print(result)


main()
