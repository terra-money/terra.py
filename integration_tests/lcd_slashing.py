from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coins, Coin
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.slashing.signing_infos()
    print(result)
    result = terra.slashing.signing_info('terravalcons1px544qs6a6m5jxfx5sjtx22mq79chsqxyszhe0')
    print(result)
    result = terra.slashing.parameters()
    print(result)

main()