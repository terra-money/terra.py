from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.ibc.parameters()
    print(result)
    # TODO: other queries have low priority


main()
