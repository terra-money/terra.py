from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.wasm.parameters()
assert "max_contract_size" in parameters
assert "max_contract_gas" in parameters
assert "max_contract_msg_size" in parameters
assert "max_contract_data_size" in parameters
assert "event_params" in parameters

code_info = bombay.wasm.code_info(1)
assert "code_id" in code_info
assert "creator" in code_info

# TODO: Add tests for contract_info and contract_query (require contracts included in genesis)
