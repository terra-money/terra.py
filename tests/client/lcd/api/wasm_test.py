from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)

def test_code_info():
    result = terra.wasm.code_info(3)
    assert result is not None


def test_contract_info():
    result = terra.wasm.contract_info("terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8")
    assert result is not None


def test_contract_query():
    result = terra.wasm.contract_query(
        "terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8",
        {"prices": {}},
    )
    assert result is not None


def test_parameters():
    result = terra.wasm.parameters()
    assert result.get("max_contract_size")
    assert result.get("max_contract_gas")
    assert result.get("max_contract_msg_size")
