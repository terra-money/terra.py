import asyncio
import base64
from pathlib import Path

from terra_sdk.client.lcd.api.tx import BroadcastOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


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
    tx = test1.create_and_sign_tx(msgs=[msg])
    print(tx)

    opt = BroadcastOptions(
        sequences=[58], fee_granter="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v"
    )

    result = terra.tx.broadcast(tx, opt)
    print(result)


main()
