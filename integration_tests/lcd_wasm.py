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
    result = terra.wasm.contract_info("terra1cz7j9y80de9e4lsec5qgw9hdy5lh4r45mvdx98")
    print(result)
    result = terra.wasm.contract_query(
        "terra1cz7j9y80de9e4lsec5qgw9hdy5lh4r45mvdx98",
        {"all_allowances": {"owner": "terra1zjwrdt4rm69d84m9s9hqsrfuchnaazhxf2ywpc"}},
    )
    print(result)
    result = terra.wasm.parameters()
    print(result)


main()
