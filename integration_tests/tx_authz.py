from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core.authz import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)


def main():
    terra = LocalTerra()
    test1 = terra.wallets["test1"]

    msgG = MsgGrantAuthorization(
        granter="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        grantee="terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp"
        """
        grant=Grant(
            authorization=...,
            expiration=
        )
        """,
    )
    msgE = MsgExecAuthorized()
    msgR = MsgRevokeAuthorization()

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgG]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgE]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = test1.create_and_sign_tx(CreateTxOptions(msgs=[msgR]))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")


main()
