from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)

def test_code_info():
    result = terra.wasm.code_info(72)

    assert result["code_id"] == 72
    assert result["creator"] == "terra1mzhc9gvfyh9swxed7eaxn2d6zzc3msgftk4w9e"
    assert result["data_hash"] == "CD686878A33E62CBCDAF7620E776096E4D15856CC03B0F12EDE66A1D5699D39D"

def test_contract_info():
    result = terra.wasm.contract_info("terra19xa33fjdjlz9qkafrw8qnrzrawc8h0vhxvfdhh6yk3f5qxuh2fps9e49zt")

    assert result is not None


def test_contract_query():
    result = terra.wasm.contract_query(
        "terra19xa33fjdjlz9qkafrw8qnrzrawc8h0vhxvfdhh6yk3f5qxuh2fps9e49zt",
        {"get_count": {}},
    )
    assert result is not None


def test_parameters():
    result = terra.wasm.parameters()
    assert result['code_ids'] is not None
