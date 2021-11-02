

""" done
import lcd_auth
import lcd_authz
import lcd_bank
import lcd_distribution
import lcd_gov
import lcd_market
import lcd_mint
import lcd_oracle
import lcd_slashing
import lcd_wasm
import lcd_treasury
import lcd_tendermint
import lcd_ibc
import lcd_ibc_transfer

"""

#import lcd_tx
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.bank import MsgSend

from terra_sdk.client.localterra import LocalTerra

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.tx import SignMode

from terra_sdk.util.json import JSONSerializable

""" untested
import lcd_gov
"""

########

from terra_sdk.core.public_key import SimplePublicKey
from terra_sdk.core import Coin, Coins

def main():
    terra = LocalTerra()
    test1 = terra.wallets["test1"]

    msg = MsgSend(
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
        Coins(uluna=30000),
    )

    opt = CreateTxOptions(
        msgs=[msg]
    )
    #tx = test1.create_tx(opt)
    tx = test1.create_and_sign_tx(opt)
    print("SIGNED TX", tx)

    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

main()