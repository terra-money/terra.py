from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.wasm import MsgExecuteContract, MsgInstantiateContract, MsgStoreCode
from terra_sdk.key.mnemonic import MnemonicKey


def main():
    terra = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-12")
    key1 = MnemonicKey(mnemonic="notice oak worry limit wrap speak medal online prefer cluster roof addict wrist behave treat actual wasp year salad speed social layer crew genius")
    test1 = terra.wallet(key1)

    execute_tx = test1.create_and_sign_tx(
        CreateTxOptions(
            msgs=[
                MsgExecuteContract(
                    test1.key.acc_address,
                    "terra1vx6kj7afw7mqekzq7mce6q2rl54fly8yhyle85",
                    "test"
                )
            ],
        )
    )
    #                {"uluna": 1000},

    execute_tx_result = terra.tx.broadcast(execute_tx)
    print(execute_tx_result)

    result = terra.wasm.contract_query("terra1zfpmxxml57vcawqg2f9nxk85t0d588r8g3ptap", "test")
    print(result)


main()
