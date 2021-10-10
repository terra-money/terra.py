import asyncio
import base64
from pathlib import Path

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Coins
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(url="https://silent-restless-snowflake.terra-mainnet.quiknode.pro/166cf94134bb9f132e27d52f456ed967332e8ba3/", chain_id="columbus-5")

    result = terra.bank.balance(address='terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    print(result)
    result = terra.treasury.parameters()
    print(result)


main()
