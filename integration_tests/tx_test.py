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


from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions

# import lcd_tx
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coin, Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.tx import SignMode
from terra_sdk.key.key import SignOptions
from terra_sdk.key.mnemonic import MnemonicKey


def main():
    terra = LocalTerra()

    seed = "quality vacuum heart guard buzz spike sight swarm shove special gym robust assume sudden deposit grid alcohol choice devote leader tilt noodle tide penalty"
    key = MnemonicKey(mnemonic=seed)

    msg = MsgSend(
        key.acc_address,
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        Coins(uluna=30000),
    )

    tx_opt = CreateTxOptions(msgs=[msg], memo="send test", gas_adjustment=1.5)

    signer_opt = SignerOptions(address=key.acc_address)

    acc_info = terra.auth.account_info(key.acc_address)

    sign_opt = SignOptions(
        account_number=acc_info.account_number,
        sequence=acc_info.sequence,
        sign_mode=SignMode.SIGN_MODE_DIRECT,
        chain_id="localterra",
    )

    tx = terra.tx.create([signer_opt], tx_opt)

    signed_tx = key.sign_tx(tx, sign_opt)

    result = terra.tx.broadcast(signed_tx)
    print(result)


main()
