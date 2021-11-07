from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coin, Coins
from terra_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)


def main():
    terra = LocalTerra()
    test1 = terra.wallets["test1"]
    validator = terra.wallets["validator"]

    msgFund = MsgFundCommunityPool(
        depositor="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        amount=Coins("1000000uusd,1000000ukrw"),
    )
    msgSet = MsgSetWithdrawAddress(
        delegator_address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        withdraw_address="terra1av6ssz7k4xpc5nsjj2884nugakpp874ae0krx7",
    )
    msgWCom = MsgWithdrawValidatorCommission(
        validator_address="terravaloper1dcegyrekltswvyy0xy69ydgxn9x8x32zdy3ua5"
    )
    msgWDel = MsgWithdrawDelegationReward(
        delegator_address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        validator_address="terravaloper1dcegyrekltswvyy0xy69ydgxn9x8x32zdy3ua5",
    )

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgFund]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgSet]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgWDel]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = validator.create_and_sign_tx(CreateTxOptions(msgs=[msgWCom]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")


main()
