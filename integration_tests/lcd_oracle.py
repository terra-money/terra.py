from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.oracle.exchange_rates()
    print(result)
    result = terra.oracle.exchange_rate("ukrw")
    print(result)
    result = terra.oracle.active_denoms()
    print(result)
    result = terra.oracle.feeder_address(
        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
    )
    print(result)
    result = terra.oracle.misses("terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw")
    print(result)
    result = terra.oracle.aggregate_prevote(
        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
    )
    print(result)
    result = terra.oracle.aggregate_vote(
        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
    )
    print(result)
    result = terra.oracle.parameters()
    print(result)


main()
