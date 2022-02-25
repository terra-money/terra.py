import asyncio
import base64
from pathlib import Path

from terra_sdk.key.mnemonic import MnemonicKey

from terra_sdk.client.lcd import LCDClient

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins
from terra_sdk.core.market import MsgSwap


def main():
    terra = LCDClient(
        chain_id="bombay-12",
        url="https://bombay-lcd.terra.dev/",
    )
    key = MnemonicKey(
        mnemonic="notice oak worry limit wrap speak medal online prefer cluster roof addict wrist behave treat actual wasp year salad speed social layer crew genius"
    )

    test1 = terra.wallet(key=key)

    print(test1)
    msg = MsgSwap(
        trader="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        offer_coin="100000uluna",
        ask_denom='uusd'
    )
    print(msg)
    tx = test1.create_and_sign_tx(CreateTxOptions(
        msgs=[msg], gas_prices="0.2uluna", gas_adjustment="1.4"
    ))
    print(tx)

    result = terra.tx.broadcast(tx)
    print(result)


main()
