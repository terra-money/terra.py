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
from terra_sdk.core.auth import (
    MsgCreatePeriodicVestingAccount,
    MsgCreateVestingAccount,
    MsgDonateAllVestingTokens,
    Period
)
def main():
    terra = LocalTerra()

    seed = "notice oak worry limit wrap speak medal online prefer cluster roof addict wrist behave treat actual wasp year salad speed social layer crew genius"
    seed_pv = "father submit repeat detail wild blast wool cat machine sphere cute tool speak slogan double common camp lab example subject winter better grit property"
    seed_v = "very police soap exchange club analyst identify injury skate sibling dash trust gauge assault work way business sniff orient female bring truth exit adult"
    key = MnemonicKey(mnemonic=seed)
    key_pv = MnemonicKey(mnemonic=seed_pv)
    key_v = MnemonicKey(mnemonic=seed_v)

    wallet = terra.wallet(key)
    wallet_pv = terra.wallet(key_pv)
    wallet_v = terra.wallet(key_v)
    print(key_pv.acc_address)
    print(key_v.acc_address)
    cva = MsgCreateVestingAccount(
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        key_v.acc_address,
        Coins("2000uluna"),
        1659130372,
        False
    )

    cpva = MsgCreatePeriodicVestingAccount(
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        key_pv.acc_address,
        1659130372,
        [Period(100, Coins("1000uluna"))]
    )

    tx = wallet.create_and_sign_tx(CreateTxOptions(
        msgs =[cva, cpva],
    ))
    result = terra.tx.broadcast(tx)

    send1 = MsgSend("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v", key_v.acc_address, Coins("100000uluna"))
    send2 = MsgSend("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v", key_pv.acc_address, Coins("100000uluna"))

    tx = wallet.create_and_sign_tx(CreateTxOptions(
        msgs =[send1, send2],
        memo= "test from terra.py"
    ))
    result = terra.tx.broadcast(tx)

    print("send to vesting and periodic vesting account : ", result)

    tx = wallet_v.create_and_sign_tx(CreateTxOptions(msgs=[
        MsgDonateAllVestingTokens(key_v.acc_address)
    ]))
    result = terra.tx.broadcast(tx)
    
    print("donate all tokens in vesting account : ", result)
    tx = wallet_pv.create_and_sign_tx(CreateTxOptions(msgs=[
        MsgDonateAllVestingTokens(key_pv.acc_address)
    ]))
    result = terra.tx.broadcast(tx)
    print("donate all tokens in periodic vesting account : ", result)


main()
