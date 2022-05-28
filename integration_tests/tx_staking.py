import base64

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.staking import (
    CommissionRates,
    Description,
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd import LCDClient


def main():
    terra = LCDClient(
        url="https://pisco-lcd.terra.dev/",
        chain_id="pisco-1",
    )

    mk1 = MnemonicKey(mnemonic="nut praise glare false post crane clinic nothing happy effort loyal point parent few series task base maximum insect glass twice inflict tragic cancel")
    mk2 = MnemonicKey(mnemonic="invite tape senior armor tragic punch actor then patrol mother version impact floor begin fitness tool street lava evidence lemon oval width soda actual")

    test1 = terra.wallet(mk1) 
    validator1_address = "terravaloper1thuj2a8sgtxr7z3gr39egng3syqqwas4hmvvlg"
    validator2_address = "terravaloper1q33jd4t8788ckkq8u935wtxstjnphcsdne3gud"
    """
    msgCV = MsgCreateValidator(
        description=Description(moniker="testval_1"),
        commission=CommissionRates(rate="0.01", max_rate="0.1", max_change_rate="0.01"),
        min_self_delegation=1,
        delegator_address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        validator_address="terravalcons1mgp3028ry5wf464r3s6gyptgmngrpnelhkuyvm",
        pubkey=ValConsPubKey(),
        value="10000000uluna"
    )

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgCV]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")
    
    """

    # msgEV = MsgEditValidator(
    #     validator_address="",
    #     description=Description(moniker="testval_1"),
    #     commission=CommissionRates(rate="0.02", max_rate="0.1", max_change_rate="0.01"),
    #     min_self_delegation=1,
    # )

    msgDel = MsgDelegate(
        validator_address=validator1_address,
        delegator_address=test1.key.acc_address,
        amount="100uluna",
    )
    msgRedel = MsgBeginRedelegate(
        validator_dst_address=validator2_address,
        validator_src_address=validator1_address,
        delegator_address=test1.key.acc_address,
        amount=Coin.parse("10uluna"),
    )

    msgUndel = MsgUndelegate(
        validator_address=validator1_address,
        delegator_address=test1.key.acc_address,
        amount=Coin.parse("20uluna"),
    )

    """

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgEV]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")
    """

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgDel]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgRedel]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgUndel]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")


main()
