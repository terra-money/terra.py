from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.params import PaginationOptions
from terra_sdk.core import Coins, Coin
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    pagOpt = PaginationOptions(limit=2, count_total=True)
    # tx - just querying APIs
    result = terra.tx.tx_info("")
    print("tx_info", result)
    result = terra.tx.txInfosByHeight()
    result = terra.tx.search()

    # tx - actual tx related
    result = terra.tx.encode()
    result = terra.tx.hash()

    result = terra.tx.estimate_fee()
    result = terra.tx.estimate_gas()
    result = terra.tx.compute_tax()
    result = terra.tx.create()

    # tx - broadcast
    result = terra.tx.broadcast()  # block-mode
    result = terra.tx.broadcast_sync()
    result = terra.tx.broadcast_async()

    print(result)

main()