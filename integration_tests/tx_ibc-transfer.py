from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core import Coin, Coins
from terra_sdk.core.ibc import Height
from terra_sdk.core.ibc_transfer import MsgTransfer
from terra_sdk.exceptions import LCDResponseError
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    key = MnemonicKey(
        mnemonic="notice oak worry limit wrap speak medal online prefer cluster roof addict wrist behave treat actual wasp year salad speed social layer crew genius"
    )

    wallet = terra.wallet(key=key)

    signedTx = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=[
                MsgTransfer(
                    source_port="transfer",
                    source_channel="channel-9",
                    token="10000uluna",
                    sender="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
                    receiver="terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
                    timeout_height=Height(revision_number=0, revision_height=10000),
                    timeout_timestamp=0,
                )
            ]
        )
    )
    try:
        result = terra.tx.broadcast(signedTx)
    except LCDResponseError as err:
        print("err: ", err)
    else:
        print("err..")

    print(result)


main()
