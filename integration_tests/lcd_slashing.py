from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    pagopt = PaginationOptions(limit=3, count_total=True, reverse=True)

    result = terra.slashing.signing_infos(pagopt)
    print(result)
    result = terra.slashing.signing_info(
        "terravalcons1lcjwqqp8sk86laggdagvk2lez0v3helfztsarh"
    )
    print(result)
    result = terra.slashing.parameters()
    print(result)


main()
