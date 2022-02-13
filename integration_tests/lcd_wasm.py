from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.wasm.code_info(3)
    print(result)
    result = terra.wasm.contract_info("terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8")
    print(result)
    result = terra.wasm.contract_query(
        "terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8",
        {"prices": {}},
    )
    print(result)
    result = terra.wasm.parameters()
    print(result)


main()
