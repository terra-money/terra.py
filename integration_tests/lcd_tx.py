from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.params import PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    pagOpt = PaginationOptions(limit=2, count_total=True)
    # tx - just querying APIs
    result = terra.tx.tx_info(
        "7AB5550F54A1B6B8A480C6B870DFFB1E94D6DB7579F9620E4172525476B8BBA2"
    )
    print("tx_info", result)
    # result = terra.tx.txInfosByHeight()
    # result = terra.tx.search()


main()
