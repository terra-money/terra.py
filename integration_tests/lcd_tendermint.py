from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.tendermint.validator_set()
    print(result)
    result = terra.tendermint.node_info()
    print(result)
    result = terra.tendermint.block_info()
    print(result)
    result = terra.tendermint.syncing()
    print(result)


main()
