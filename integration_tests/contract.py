import asyncio
import base64

from pathlib import Path

from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract


async def main():
    async with LocalTerra() as terra:
        test1 = terra.wallets["test1"]
        contract_file = open(Path(__file__).parent / "./contract.wasm", "rb")
        file_bytes = base64.b64encode(contract_file.read())
        store_code = MsgStoreCode(test1.key.acc_address, file_bytes)
        store_code_tx = await test1.create_and_sign_tx(msgs=[store_code])
        store_code_tx_result = await terra.tx.broadcast(store_code_tx)
        print(store_code_tx_result)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())