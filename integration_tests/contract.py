import asyncio
import base64

from pathlib import Path

from terra_sdk.core import Coins
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core.auth import StdFee
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract


async def main():
    async with LocalTerra() as terra:
        test1 = terra.wallets["test1"]
        contract_file = open(Path(__file__).parent / "./contract.wasm", "rb")
        file_bytes = base64.b64encode(contract_file.read()).decode()
        store_code = MsgStoreCode(test1.key.acc_address, file_bytes)
        store_code_tx = await test1.create_and_sign_tx(msgs=[store_code])
        store_code_tx_result = await terra.tx.broadcast(store_code_tx)
        print(store_code_tx_result)

        code_id = store_code_tx_result.logs[0].events_by_type["store_code"]["code_id"][
            0
        ]
        instantiate = MsgInstantiateContract(
            test1.key.acc_address,
            code_id,
            {"count": 0},
            {"uluna": 10000000, "ukrw": 1000000},
            False,
        )
        instantiate_tx = await test1.create_and_sign_tx(msgs=[instantiate])
        instantiate_tx_result = await terra.tx.broadcast(instantiate_tx)
        print(instantiate_tx_result)

        contract_address = instantiate_tx_result.logs[0].events_by_type[
            "instantiate_contract"
        ]["contract_address"][0]

        execute = MsgExecuteContract(
            test1.key.acc_address,
            contract_address,
            {"increment": {}},
            {"uluna": 100000},
        )

        execute_tx = await test1.create_and_sign_tx(
            msgs=[execute], fee=StdFee(1000000, Coins(uluna=1000000))
        )

        execute_tx_result = await terra.tx.broadcast(execute_tx)
        print(execute_tx_result)

        result = await terra.wasm.contract_query(contract_address, {"get_count": {}})
        print(result)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())