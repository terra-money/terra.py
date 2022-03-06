import asyncio
from pathlib import Path

import uvloop

from terra_sdk.client.lcd import AsyncLCDClient
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.wasm import MsgExecuteContract, MsgInstantiateContract, MsgStoreCode
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.util.contract import get_code_id, get_contract_address, read_file_as_b64


async def main():
    terra = AsyncLCDClient(url="http://localhost:1317", chain_id="localterra")
    terra.gas_prices = "1uluna"
    # test1 = terra.wallets["test1"]
    acc = MnemonicKey(
        mnemonic="rotice oak worry limit wrap speak medal online prefer cluster roof addict wrist behave treat actual wasp year salad speed social layer crew genius"
    )
    test1 = terra.wallet(acc)

    store_code_tx = await test1.create_and_sign_tx(
        CreateTxOptions(
            msgs=[
                MsgStoreCode(
                    test1.key.acc_address,
                    read_file_as_b64(Path(__file__).parent / "./contract.wasm"),
                )
            ],
            gas_adjustment=1.75,
        )
    )
    store_code_tx_result = await terra.tx.broadcast(store_code_tx)
    print(store_code_tx_result)

    code_id = get_code_id(store_code_tx_result)
    print(f"cod_id:{code_id}")

    instantiate_tx = await test1.create_and_sign_tx(
        CreateTxOptions(
            msgs=[
                MsgInstantiateContract(
                    test1.key.acc_address, test1.key.acc_address, code_id, {"count": 10}
                )
            ],
            gas_prices="10uluna",
            gas_adjustment=2,
        )
    )
    print(instantiate_tx)
    instantiate_tx_result = await terra.tx.broadcast(instantiate_tx)
    print(instantiate_tx_result)
    contract_address = get_contract_address(instantiate_tx_result)
    # """
    # contract_address = "terra1e8d3cw4j0k5fm9gw03jzh9xzhzyz99pa8tphd8"
    result = await terra.wasm.contract_query(contract_address, {"get_count": {}})
    print("get_count1: ", result)
    execute_tx = await test1.create_and_sign_tx(
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
    #                {"uluna": 1000},

    execute_tx_result = await terra.tx.broadcast(execute_tx)
    print(execute_tx_result)

    result = await terra.wasm.contract_query(contract_address, {"get_count": {}})
    print("get_count2: ", result)

    await terra.session.close()


uvloop.install()
asyncio.run(main())
