import asyncio
import base64
from pathlib import Path

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="columbus-5",
    )

    result = terra.bank.balance(address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
    print(result)
    result = terra.treasury.parameters()
    print(result)


main()
