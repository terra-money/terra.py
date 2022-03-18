from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.util.contract import get_code_id, read_file_as_b64
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from terra_sdk.core.coins import Coins
from terra_sdk.core.fee import Fee

lt = LocalTerra()
deployer = lt.wallets["test1"]
test_acc = lt.wallets["test2"]


def store_contract(contract_name):
    contract_bytes = read_file_as_b64(f"artifacts/{contract_name}.wasm")
    store_code = MsgStoreCode(deployer.key.acc_address, contract_bytes)
    tx = deployer.create_and_sign_tx(CreateTxOptions(
        msgs=[store_code]
    ))
    result = lt.tx.broadcast(tx)
    code_id = get_code_id(result)
    return code_id


def instantiate_contract(code_id: str, init_msg: dict) -> str:
    instantiate = MsgInstantiateContract(
        sender=deployer.key.acc_address,
        admin=deployer.key.acc_address,
        code_id=code_id,
        init_msg=init_msg,
    )

    tx = deployer.create_and_sign_tx(CreateTxOptions(
        msgs=[instantiate]
    ))

    result = lt.tx.broadcast(tx)
    print(result)
    return result


def execute_contract(sender, contract_addr: str, execute_msg):

    execute = MsgExecuteContract(
        sender=sender.key.acc_address, contract=contract_addr, execute_msg=execute_msg
    )
    # tx = sender.create_and_sign_tx(CreateTxOptions(
    #     msgs=[execute],
    #     fee=Fee(1000000, "1000000uluna")
    # ))
    execute = MsgExecuteContract(
        sender.key.acc_address,
        contract_addr,
        execute_msg,
        {"uluna": 100000},
    )

    execute_tx = sender.create_and_sign_tx(
        CreateTxOptions(msgs=[execute], fee=Fee(1000000, Coins(uluna=1000000)))
    )

    result = lt.tx.broadcast(execute_tx)
    print(result)
    return result


code_id = store_contract("terraswap_token")
contract_address = instantiate_contract(code_id,
                                        {
                                            "name": "Test Terra Token",
                                            "symbol": "TTT",
                                            "decimals": 6,
                                            "initial_balances": [
                                                {"address": deployer.key.acc_address,
                                                    "amount": "1000000000"}
                                            ]
                                        })

execute_contract(deployer, contract_address, {
    "transfer": {
        "recipient": test_acc.key.acc_address,
        "amount": "50000000000"
    }
})

print(lt.wasm.contract_query(contract_address, {
      "balance": {"address": deployer.key.acc_address}}))

print(lt.wasm.contract_query(contract_address, {
      "balance": {"address": test_acc.key.acc_address}}))
