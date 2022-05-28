from pathlib import Path

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins
from terra_sdk.core.fee import Fee
from terra_sdk.core.wasm import MsgExecuteContract, MsgInstantiateContract, MsgStoreCode
from terra_sdk.core.wasm.data import AccessConfig
from terra_sdk.util.contract import get_code_id, get_contract_address, read_file_as_b64

from terra_proto.cosmwasm.wasm.v1 import (
    AccessType
)

def main():
    terra = LocalTerra()
    terra.gas_prices = "1uluna"
    test1 = terra.wallets["test1"]

    store_code_tx = test1.create_and_sign_tx(
        CreateTxOptions(
            msgs=[
                MsgStoreCode(
                    test1.key.acc_address,
                    read_file_as_b64(Path(__file__).parent / "./contract.wasm"),
                    AccessConfig(AccessType.ACCESS_TYPE_EVERYBODY,"")
                )
            ],
            gas_adjustment=1.75,
        )
    )
    store_code_tx_result = terra.tx.broadcast(store_code_tx)
    print(store_code_tx_result)

    code_id = get_code_id(store_code_tx_result)
    print(f"cod_id:{code_id}")

    instantiate_tx = test1.create_and_sign_tx(
        CreateTxOptions(
            msgs=[
                MsgInstantiateContract(
                    test1.key.acc_address,
                    test1.key.acc_address,
                    code_id,
                    "testlabel",
                    {"count": 10},
                    "10uluna"
                )
            ],
            gas_prices="10uluna",
            gas_adjustment=2,
        )
    )
    print(instantiate_tx)
    instantiate_tx_result = terra.tx.broadcast(instantiate_tx)
    print(instantiate_tx_result)
    contract_address = get_contract_address(instantiate_tx_result)
    # """
    # contract_address = "terra1e8d3cw4j0k5fm9gw03jzh9xzhzyz99pa8tphd8"
    print("contract_address = ", contract_address)
    result = terra.wasm.contract_query(contract_address, {"get_count": {}})
    print("get_count1: ", result)
    execute_tx = test1.create_and_sign_tx(
        CreateTxOptions(
            msgs=[
                MsgExecuteContract(
                    test1.key.acc_address,
                    contract_address,
                    {"increment": {}},
                )
            ],
            gas_adjustment=1.75,
        )
    )

    execute_tx_result = terra.tx.broadcast(execute_tx)
    print(execute_tx_result)

    result = terra.wasm.contract_query(contract_address, {"get_count": {}})
    print("get_count2: ", result)


# try:
main()
# except Exception as e:
#    print("exception occured")
#    print(e)
