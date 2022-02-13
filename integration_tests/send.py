import asyncio
import base64
from pathlib import Path

from terra_sdk.core.tx import SignMode
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins
from terra_sdk.core.bank import MsgSend


def main():
    terra = LocalTerra()
    test1 = terra.wallets["test1"]

    print(test1)
    msg = MsgSend(
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
        Coins(uluna=1000000),
    )
    print(msg)
    tx = test1.create_and_sign_tx(CreateTxOptions(
        msgs=[msg], gas_prices="0.2uluna", gas_adjustment="1.4",
        sign_mode=SignMode.SIGN_MODE_LEGACY_AMINO_JSON
    ))
    print(tx)

    result = terra.tx.broadcast(tx)
    print(result)


main()
