""" done
import lcd_auth
import lcd_authz
import lcd_bank
import lcd_distribution
import lcd_gov
import lcd_mint
import lcd_slashing
import lcd_wasm
import lcd_tendermint
import lcd_ibc
import lcd_ibc_transfer

"""


from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions

# import lcd_tx
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.tx import SignMode
from terra_sdk.key.key import SignOptions
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.feegrant.data import Allowance, BasicAllowance
from terra_sdk.core.feegrant.msgs import MsgGrantAllowance, MsgRevokeAllowance

def main():
    terra = LocalTerra()

    seed = "quality vacuum heart guard buzz spike sight swarm shove special gym robust assume sudden deposit grid alcohol choice devote leader tilt noodle tide penalty"
    key = MnemonicKey(mnemonic=seed)
    test1 = terra.wallets["test1"]
    test2 = terra.wallets["test2"]
    test1_address = test1.key.acc_address
    test2_address = test2.key.acc_address

    msg = MsgGrantAllowance(
        granter = test1_address,
        grantee = test2_address,
        allowance = BasicAllowance(None, "2020-02-02T07:58:20Z")
    )

    opt = CreateTxOptions(
        msgs=[msg], memo="send test", gas_adjustment=1.5, gas_prices="1uluna"
    )
    # tx = test1.create_tx(opt)
    tx = test1.create_and_sign_tx(opt)
    print("SIGNED TX", tx)

    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")


main()
