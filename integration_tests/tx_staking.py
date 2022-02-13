import base64

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coin, Coins, ValConsPubKey
from terra_sdk.core.staking import (
    CommissionRates,
    Description,
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)


def main():
    terra = LocalTerra()
    test1 = terra.wallets["test1"]
    """
    msgCV = MsgCreateValidator(
        description=Description(moniker="testval_1"),
        commission=CommissionRates(rate="0.01", max_rate="0.1", max_change_rate="0.01"),
        min_self_delegation=1,
        delegator_address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        validator_address="terravalcons1mgp3028ry5wf464r3s6gyptgmngrpnelhkuyvm",
        pubkey=ValConsPubKey(),
        value="10000000uusd"
    )

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgCV]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")
    
    """

    msgEV = MsgEditValidator(
        validator_address="",
        description=Description(moniker="testval_1"),
        commission=CommissionRates(rate="0.02", max_rate="0.1", max_change_rate="0.01"),
        min_self_delegation=1,
    )

    msgDel = MsgDelegate(
        validator_address="terravaloper1dcegyrekltswvyy0xy69ydgxn9x8x32zdy3ua5",
        delegator_address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        amount="10000000uluna",
    )
    msgRedel = MsgBeginRedelegate(
        validator_dst_address="terravaloper1dcegyrekltswvyy0xy69ydgxn9x8x32zdy3ua5",
        validator_src_address="terravaloper1dcegyrekltswvyy0xy69ydgxn9x8x32zdy3ua5",
        delegator_address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        amount=Coin.parse("1000000uluna"),
    )

    msgUndel = MsgUndelegate(
        validator_address="terravaloper1dcegyrekltswvyy0xy69ydgxn9x8x32zdy3ua5",
        delegator_address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        amount=Coin.parse("10000000uluna"),
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
